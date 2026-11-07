from pathlib import Path

from django.db import migrations


def restore_title_column(apps, schema_editor):
    Recording = apps.get_model("recorder", "Recording")
    connection = schema_editor.connection
    table_name = Recording._meta.db_table

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        }

    if "title" not in columns:
        quote_name = schema_editor.quote_name
        title_type = Recording._meta.get_field("title").db_type(connection)
        schema_editor.execute(
            f"ALTER TABLE {quote_name(table_name)} "
            f"ADD COLUMN {quote_name('title')} {title_type} NOT NULL DEFAULT 'Recording'"
        )

    database = connection.alias
    for recording in Recording.objects.using(database).only("pk", "audio_file").iterator():
        title = Path(recording.audio_file.name).name[:100] or "Recording"
        Recording.objects.using(database).filter(pk=recording.pk).update(title=title)


class Migration(migrations.Migration):
    dependencies = [
        ("recorder", "0002_alter_recording_options_recording_transcript"),
    ]

    operations = [
        migrations.RunPython(restore_title_column, migrations.RunPython.noop),
    ]
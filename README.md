## Run Instructions

From the project directory, create and activate a virtual environment, then install the project dependencies. Here is an example of inputs for a windows computer:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

You can access the webpage through <http://127.0.0.1:8000/> and allow microphone access. Press the (Record) button to start recording and (Stop) to finish. Recordings are then stored locally and transcribed using Whisper.


## Design Decisions

The first notable decision I made when creating this web page was to use Django as my framework. I chose Django as the framework because it could easily handle the backend operations required for the application, including storing recordings and transcripts, while also being a framework I am familiar with. My next challenge was figuring out exactly how I would go about recording audio. For this task, I decided to used the MediaRecorder API. This provided a straightforward way to capture microphone input without requiring additional client-side dependencies. From there I set out on the task of recording, storing, and transcribing the data. As requested, I used faster-whisper with the tiny.en model. After recording, the audio is processed and normalized into a mono WAV file for playback. I made this change after encountering issues with reliably retrieving and processing the original recordings. Using a consistent audio format also makes the input to the transcription process more dependable.


## Future Iterations

If given more time, I have various changes I would have made to both the front end and the back end. Starting with the front end, I would have liked to make the interface a lot more visually polished and easier to navigate. My initial plan was to create a scrollable list of previous recordings on the left side of the page, and the right side would display the recording and the transcription of the currently selected audio. Additionally, I would have liked to add a feature that allows users to more easily export the transcription of their audio to a document. 

For the backend portion of the code, I would have liked to add a thorough set of tests to check for upload, conversion, and transcription failures. I would also improve error handling so that useful error messages are displayed to the user instead of simply reloading the page when something goes wrong.


## AI Usage

I completed the majority of this project without the usage of AI. I briefly used the built-in agent in VS Code during the debugging stages to help identify and resolve issues.

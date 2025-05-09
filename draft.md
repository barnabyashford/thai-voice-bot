# Leveraging LLM in developing “Virtual Friend” for Idle Conversation

Worrapat Cheng  
> Language and Information Technology Major,  
> Faculty of Arts,  
> Chulalongkorn University

## Abstract



> **Keywords:** Artificial Intelligence, Automatic Speech Recognition, Chatbot, Large Language Model, Multimodal, Natural Language Processing, Text-to-Speech

## Introduction

Since the advent of Large Language Models (LLM), many efforts have been made to either improve LLM's performance at language generation and comprehension, or devise techniques to optimise resource usage of LLM. As LLM evolves over the years, there have also been efforts to extend the linguistic capability beyond the boundary of text. This project aims to do exactly that, although not directly. With the purpose to let LLM be implemented in a chatbot application that is not based on textual conversation, but rather a voice conversation, a "Voice bot". As an introduction, this paper starts by explaining each major component: Speech Recognizer, Large Language Model, and Speech Synthesizer.

### Speech Recognizer

"Speech recognizer" refers to a program, an agent, or an artificial intelligence technology that is designed to perform the task of speech recognition, **automatically** and accordingly transcribes into text the input speech audio. Hence also being known as **Automatic Speech Recognition** (ASR) model.

### Large Language Model (LLM)

Pragmatically refers to any transformers-based autoregressive language model that is trained on a tremendous amount of natural language data, resulting in a language model with a number of parameter as high as billions or even trillions. Known widely for their ability to produce language with fluency closely resemble that of a human.

### Speech Synthesizer

Also known as the Text-to-Speech (TTS) model, both terminologies overlap in referent of an artificial intelligent model designed and tasked to take text input in order to "synthesize" a corresponding speech audio. 

## Problem Definition 

LLMs are trained on textual data, hence their proficiency in generating and understanding natural language in the form of text. That is, however, not the focus of this project, which is rather "speech". To address this, this project was carried on with these objectives, (1) to find a solution to develop an application that implements LLM as the response generator while allowing input as speech and output as the same, extending the possibility of practical LLM implementation beyond text and (2) to test and evaluate the usability of the application developed under the solution with the use case of having the voice bot act as the user's best friend. The key of this use case is that the bot must be able to engage the user in **idle** conversation. That is, the bot, while able to "listen" and "speak" back to the user, must not only listen and answer to the user's input, but invite amd engage the user and/or pose question to continue the conversation be itself as well. Being the user's **Virtual Friend**.

## Application Design

The architecture design stages of this project can be divided into two major states; the "manual I/O" stage and the "press and converse" stage. Both stages relates to each other chronologically, as the latter derived from the prior as the objectively superior design in user experience. Note that the latter was not created abruptly after the prior, but rather an improvement after implementation. Moreover, both design emphasizes intensively on dividing the three main component of the application apart in a modular manner. This was intended to make the pipeline applicable with other model, making each component easily replaceable with different choice as one see fit.

### The Manual Input/Output Design

This design was developed as an intuitive initial flow of the application. As the name suggests, the flow of this design involves the user manually pressing a button to start recording, then repeating the action to stop recording. The application will then send the recording to the speech recognizer in order to receive a corresponding transcript. Subsequently, the transcript will then be sent as the prompt for the LLM to generate a response to the user's input. Finally, the text response from the LLM will be sent to the speech recognizer in order to synthesize a speech response for the user to press a button to play the response audio file. Figure 1 summarizes the flow of this design visually.

![DB DFD - Page 11](https://github.com/user-attachments/assets/44a97e6e-9f75-4537-82a3-ac523016430a)

### Press \& Converse Design

To minimize the number of non-voice user interaction for the sake of user experience (i.e., convenience), this stage of design was created with the idea of letting the user manually interact with the interface only for a small fixed number of steps, which is pressing the button to start the app, then the user will be able to engage the voice bot in conversation in as many turns as the user desires. Should the user wish to terminate the conversation, the user needs only to say the keyword. The application will cease to work and shut itself down. The internal process works similarly to that of the earlier design, as appears in figure 2.

![DB DFD - Page 10 (7)](https://github.com/user-attachments/assets/d4b29d23-6e1e-46e4-965b-b7af63fdf2d4)

## Implementation

With potential designs established, proper implementations must follow as proof of concepts (POCs) to validate the idea. In creating POC of each design, each major component, i.e. speech recognizer, LLM, and speech synthesizer, are selected from available platforms or services for ease of development and controllable cost. Moreover, this project is developed entirely on the Python programming language, again, for ease of development as it is a programming language with one of, if not the biggest community contributing to many different modules and libraries, especially data- and machine-learning-related libraries.

### Manual I/O

In the first design flow, `openai/whisper-large-v3-turbo` was chosen as the speech recognizer for its popularity, as well as its accessibility and cost-friendliness. That is, the model is accessible free-of-charge via Hugging Face's Inference API. Note that the API is meant to be a demo, while technically usable for the POC, problems like request traffic, i.e. too many requests, are likely to happen. Therefore it is advisable that the model is loaded locally, or utilized via OpenAI's paid API service, whichever is suitable for one's budget, for a smoother and more stable flow of implementation. For response generation, `gemini-1.5-flash-8b` was chosen as it is available free-of-charge for each google account via API service. This guarantees fluent response from cloud-run LLM without significant risk of encountering system hiccups like those of this design's speech recognizer. Finally, `gTTS`, a python library for text-to-speech, was chosen as the speech synthesizer for convenience of use and how it uses Google Translate's speech from text and corresponding language feature to get synthetic speech for each input text. Additionally, for a more user-friendly POC, `gradio`, a python library for user interface, was implemented. The source code is provided as Google Colaboratory.

After Implementation of the first design flow, the major concern is that the number of manual user intereaction with the application increases as turns of conversation increase. That is, the more turns there is in a conversation with the voice bot, the more times the user needs to press buttons to record their speech and play the response. While works as designed and did let LLM work as response generator in an implementation that uses other mode of conversation that is speech and not text, this is far from actual voice conversation between humans where both parties (i.e., the speaker and the audience) need only speak what they mean adn listen to the other. Moreover, using Hugging Face's Inference API as the provider for speech recognition task, while not as often as not, has significant risk to return an error stating that the traffic is overcrowded. To mitigate this, developer needs only to run the model locally, or pay for OpenAI's API service, which adds to the cost if this project is ever applied on a real service.

### Press \& Converse

Derived from concerns of the earlier design, this design flow was developed these ideas in mind; (1) let the user interact with the applciation interface manually only in a limited number of steps for settings and starting the conversation. (2) Imitate human-to-human speech converation of having one party speak and another listen, then then prior audience becomes the speaker after the prior speaker has finished talking. The source code for this design is kept in the project's GitHub repository.

To achieve this, the speech recognizer was changed to **GCP Speech Recognition Service** as it supports streaming transcription, enabling the voice bot the transcribe users speech syllable-by-syllable in near real-time manner, significantly minimizes latency as the prior design requires that the speech recording process and the transcription process happen sequentially, not simultaneously. As for LLM, the model chosen for this implementation was `gemini-2.0-flash` as it was established as no longer an experimental model at the time of implementation. Moreover, as the successor of `gemini-1.5-flash`, a bigger version of `gemini-1.5-flash-8b`, this choice came with an expectation that the newer model performs better than its predecessor. For the speech synthesis task, in early implementation the same library as the prior design, `gTTS`, was selected once again for its adequate voice quality. That is, the synthetic voice created using this library (or Google Translate) was close enough to native Thai speaker to be used as POC. Although the speech synthesizer will finally be changed to using **GCP Chirp 3 HD Voices** for its objectively more natural speech quality. Note that the reason GCP's products are implemented in this specific POC because of its generous free-trail of 3 months with 300\$ worth of free credits, making the development of this project accessible to high-quality agents free-of-charge.

As per user interface development, the choice has been changed to simple command line with ANSI color-coding for component distinctguishing. To let the user be aware of voice activity, updates of transcript appear and change as the user speaks. The rationale behind this is that `gradio`, the library used in implementation of prior design does not support ChatGPT style real-time voice activity indication out-of-the-box. Moreover, using the real-time transcript update done via command line will only complicates the development.

As mentioned earlier, the only times that the user is required to manually interact with the interface are setting up the voice bot and confirming to start the conversation. In setting up the voice bot, each time the application is booted up, the user will be asked to confirm whether to move on with default system instruction, which is 

```plaintext
ทำตัวเป็นเพื่อนสนิทของผู้ใช้ การสนทนานี้เป็นการคุยกันด้วยเสียง ฉะนั้นตอบไม่เกินสองประโยค ชวนผู้ใช้คุยด้วยตนเอง
```

Alternatively, user can provide their own custom instruction should the user desire to converse with the voice bot in a different scenario. After prompt customization, the user will be asked to input `y` or `Y` as a confirmation to start the conversation.

During conversation state, the user needs only speak to the voice bot, the interim transcript will be update as the user speaks to ensure the user that the application is running. After the user has finished talking the speech recognizer will return final transcript and the application will then disable the microphone and send the final transcript to the LLM for response generation. Ultimately, the text response from the LLM will be sent to speech synthesizer module to synthesize and save as `.mp3` file and automatically play the response. This loop will go on over and over as the user desires until the user say the termination keyword to shut down the application.

As mentioned above that the speech recognizer powered by GCP's service supports streaming transcription and the flow of this design requires that the user does not interact with the interface. This means the application will decides by itself when the user has finished talking. This process is based on GCP's Speech Recognition Service's ability to decide whether the certain point of the input audio is the end of an utterance.

## Testing \& Evaluation

After the proof of concept has been developed, the concept will be tested and evaluated for its usability. As the "Press and Converse" design derived from its predecessor, the "Manual Input/Output" design, and has been established as the canonical design flow of the application, this section will only evaluate the performance of the application developed under this design and not the prior.

The evaluation will be carried out in accordance with the objectives of this project. That is, to design an architecture for voice bot development and test its usability with the use case of "Virtual Friend". To address this, three simple usability testing roleplaying cases has been prepared to see if the voice bot is able to be the user's friend. This is to test not only whether the bot is able to act in accordance with it's instruction, but also to keep statistics of each turn's response generation time and speech synthesis time. The usability testing cases include only an instruction with the differences in theme and objective.

## Discussion

## Conclusion

## Acknowledgement

## Reference

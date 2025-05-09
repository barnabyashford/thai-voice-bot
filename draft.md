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

LLMs are trained on textual data, hence their proficiency in generating and understanding natural language in the form of text. That is, however, not the focus of this project, which is rather "speech". To address this, this project was carried on with these objectives, (1) to find a solution to develop an application that implements LLM as the response generator while allowing input as speech and output as the same, extending the possibility of practical LLM implementation beyond text and (2) to test and evaluate the usability of the application developed under the solution.

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

In the first design flow, `openai/whisper-large-v3-turbo` was chosen as the speech recognizer for its popularity, as well as its accessibility and cost-friendliness. That is, the model is accessible free-of-charge via Hugging Face's Inference API. Note that the API is meant to be a demo, while technically usable for the POC, problems like request traffic, i.e. too many requests, are likely to happen. Therefore it is advisable that the model is loaded locally, or utilized via OpenAI's paid API service, whichever is suitable for one's budget, for a smoother and more stable flow of implementation. For response generation, `gemini-1.5-flash-8b` was chosen as it is available free-of-charge for each google account via API service. This guarantees fluent response from cloud-run LLM without significant risk of encountering system hiccups like those of this design's speech recognizer. Finally, `gTTS`, a python library for text-to-speech, was chosen as the speech synthesizer for convenience of use and how it uses Google Translate's speech from text and corresponding language feature to get synthetic speech for each input text. Additionally, for a more user-friendly POC, `gradio`, a python library for user interface, was implemented.

After Implementation of the first design flow, the major concern is that the number of manual user intereaction with the application increases as turns of conversation increase. That is, the more turns there is in a conversation with the voice bot, the more times the user needs to press buttons to record their speech and play the response. While works as designed and did let LLM work as response generator in an implementation that uses other mode of conversation that is speech and not text, this is far from actual voice conversation between humans where both parties (i.e., the speaker and the audience) need only speak what they mean adn listen to the other. Moreover, using Hugging Face's Inference API as the provider for speech recognition task, while not as often as not, has significant risk to return an error stating that the traffic is overcrowded. To mitigate this, developer needs only to run the model locally, or pay for OpenAI's API service, which adds to the cost if this project is ever applied on a real service.

### Press \& Converse

Derived from concerns of the earlier design, this design flow was developed these ideas in mind; (1) let the user interact with the applciation interface manually only in a limited number of steps for settings and starting the conversation. (2) Imitate human-to-human speech converation of having one party speak and another listen, then then prior audience becomes the speaker after the prior speaker has finished talking.

To achieve this, the speech recognizer was changed to **GCP Speech Recognition Service** as it supports streaming transcription, enabling the voice bot the transcribe users speech syllable-by-syllable in near real-time manner, significantly minimizes latency as the prior design 

## Testing \& Evaluation

## Discussion

## Conclusion

## Acknowledgement

## Reference

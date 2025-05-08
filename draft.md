# Leveraging LLM in developing “Virtual Friend” for Idle Conversation

Worrapat Cheng  
> Language and Information Technology Major,  
> Faculty of Arts,  
> Chulalongkorn University

## Abstract



> **Keywords:** Artificial Intelligence, Automatic Speech Recognition, Chatbot, Large Language Model, Multimodal, Natural Language Processing, Text-to-Speech

## Introduction

Since the advent of Large Language Models (LLM), many efforts have been made to either improve LLM's performance at language generation and comprehension, or devise techniques to optimise resource usage of LLM. As LLM evolves over the years, there have also been efforts to extend the linguistic capability beyond the boundary of text. This project aims to do exactly that, although not directly. With the purpose to let LLM be implemented in a chatbot application that is not based on textual conversation, but rather a voice conversation, a "Voice bot". As an introduction, this paper starts by explaining each component: Speech Recognizer, Large Language Model, and Speech Synthesizer.

### Speech Recognizer

"Speech recognizer" refers to a program, an agent, or an artificial intelligence technology that is designed to perform the task of speech recognition, **automatically** and accordingly transcribes into text the input speech audio. Hence also being known as **Automatic Speech Recognition** (ASR) model.

### Large Language Model (LLM)

Pragmatically refers to any transformers-based autoregressive language model that is trained on a tremendous amount of natural language data, resulting in a language model with a number of parameter as high as billions or even trillions. Known widely for their ability to produce language with fluency closely resemble that of a human.

### Speech Synthesizer

Also known as the Text-to-Speech (TTS) model, both terminologies overlap in referent of an artificial intelligent model designed and tasked to take text input in order to "synthesize" a corresponding speech audio. 

## Problem Definition 

LLMs are trained on textual data, hence their proficiency in generating and understanding natural language in the form of text. That is, however, not the focus of this project, which is rather "speech". To address this, this project carries on with these objectives. First, to find a solution to develop an application that implements LLM as the response generator while allowing input as speech and output as the same, extending the possibility of practical LLM implementation beyond text. Secondly and finally, test and evaluate the usability of the application developed under the solution.

## Application Design
The architecture design stages of this project can be divided into two major states; the manual I/O stage and the press and converse stage. Both stages relates to each other chronologically, as the latter derives from the prior, as the objectively superior design in user experience and latency. Note that the latter does not happen abruptly after the prior, but rather an improvement after proper implementation.

### The Manual Input/Output Design

This design was developed as a intuitive initial flow of the application. As the name suggests, the flow of this design involves the user manually pressing a button to start recording and repeat the action to stop recording, the application will then send the recording to the speech recognizer in order to receive a corresponding transcript. Subsequently, the transcript will then be sent as the prompt to the LLM to generate a response to the user's input. Finally, the text response from the LLM will then be sent to the speech recognizer in order to synthesize a speech response for the user to press a button to play the response audio file. Figure 1 summarizes the flow of this design visually.

![DB DFD - Page 11](https://github.com/user-attachments/assets/44a97e6e-9f75-4537-82a3-ac523016430a)

### Press \& Converse Design

To minimize the number of required user interaction for the sake of user experience (i.e., convenience), this stage of design is meant to let the user move their finger only once, to press the button to start the app, then the user will be able to engage the voice bot in conversation in as many turn as the user desires. Should the user wish to terminate the conversation, the user needs only to say the keyword. The application will cease to work and shut itself down. The internal process works similarly to that of the earlier design, as appears in figure 2.

![DB DFD - Page 10 (7)](https://github.com/user-attachments/assets/d4b29d23-6e1e-46e4-965b-b7af63fdf2d4)

## Implementation

With a design established, the implementation follows to as a proof of concept (POC) to valiadate the idea. In creating POC of the design, we

## Testing \& Evaluation

## Discussion

## Conclusion

## Acknowledgement

## Reference

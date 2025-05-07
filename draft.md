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

"Speech recognizer" refers to a program, an agent, or an artificial intelligence technology that is designed to the task of speech recognition, **automatically** and accordingly transcribe into text the input speech audio. Hence also being known as **Automatic Speech Recognition** (ASR) model.

### Large Language Model (LLM)

Pragmatically refers to any transformers-based autoregressive language model that is trained on a tremendous amount of natural language data, resulting in a language model with the number of parameter as high as billions or even trillions. Known widely for their capability to preduce language with fluency closely resembles that of human's.

### Speech Synthesizer

Also known as Text-to-Speech model, both terminologies overlaps in referent of an artificial intelligent model designed and tasked to take text input in order to "synthesize" a corresponding speech audio. 

## Problem Definition 

LLMs are trained on textual data hence their proficiency in generating and understanding natural language in the form of text. That is, however, not the focus of this project, which is rather "speech". To address to this, this project carries on with these objectives. First, to find a solution to developing an application that implements LLM as the response generator while allowing input as speech and output as the same, extending the possibility of practical LLM implementation beyond text. Secondly and finally, test and evaluate the usability of the application developed under the solution.

## Application Architecture
The architecture design stages of this project can be divided into two major states; the manual I/O stage and the push and converse stage. Both stages relates to each other chronologically, as the latter derives from the prior, as the objevtively superior design in user experience and latency.

### The Manual Input/Output Design

This design was developed as a intuitive initial flow of the application. As the name suggests, the flow of this design involves the user manually pressing a button to start recording and repeat the action to stop recording, the application will then invoke a POST method to utilize an ASR model API in order to receive a 

### Changes in the flow

## Implementation

## Testing \& Evaluation

## Discussion

## Conclusion

## Reference

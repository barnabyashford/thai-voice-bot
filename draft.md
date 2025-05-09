# Leveraging LLM in developing “Virtual Friend” for Idle Conversation

Worrapat Cheng  
> Language and Information Technology Major,  
> Faculty of Arts,  
> Chulalongkorn University

## Abstract

In this project, a solution to develop a voice bot, an application that, like a chatbot, but the "chat" is done in speech rather than text, is designed with three main components: a speech recognizer, a large language model, and a speech synthesizer. The application was developed on the solution design and was tested its usability. The usability testing results were then used to evaluate and reflected on each component and the application as a whole. The application succeeded in working as a speech conversational agent with latency and response quality in both content and speech closely resembles that of a human, while there exist flaws and room for requirements in: transcription quality, noise-ignoring, voice distinguising, response processing, and synthetic voice naturalness. Moreover, future works are discussed on improving each component's performance, possibility of end-to-end model, and barge-in feature.

> **Keywords:** Artificial Intelligence, Automatic Speech Recognition, Chatbot, Large Language Model, Multimodal, Natural Language Processing, Text-to-Speech

## Introduction

Since the advent of Large Language Models (LLM), many efforts have been made to either improve LLM's performance at language generation and comprehension, or devise techniques to optimise resource usage of LLM. As LLM evolves over the years, there have also been efforts to extend the linguistic capability beyond the boundary of text. This project aims to do exactly that, although not directly. With the purpose to let LLM be implemented in a chatbot application that is not based on textual conversation, but rather a voice conversation, a "Voice bot". As an introduction, this paper starts by explaining each major component: Speech Recognizer, Large Language Model, and Speech Synthesizer.

### Speech Recognizer

"Speech recognizer" refers to a program, an agent, or an artificial intelligence technology that is designed to perform the task of speech recognition, **automatically** and accordingly transcribes into text the input speech audio. Hence also being known as **Automatic Speech Recognition** (ASR) model. (IBM, n.d.; Rella, 2023)

### Large Language Model (LLM)

Pragmatically refers to any transformers-based autoregressive language model that is trained on a tremendous amount of natural language data, resulting in a language model with a number of parameter as high as billions or even trillions. Known widely for their ability to produce language with fluency closely resemble that of a human. (Amazon Web Services, n.d.)

### Speech Synthesizer

Also known as the Text-to-Speech (TTS) model, both terminologies overlap in referent of an artificial intelligent model designed and tasked to take text input in order to "synthesize" a corresponding speech audio. (IBM, n.d.)

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

### Manual I/O [^1]

[^1]: The source code is provided as [Google Colaboratory](https://colab.research.google.com/drive/1axXDr4Lw-INgR8F_vkSEM81ZnSsUELBM?usp=sharing).

In the first design flow, `openai/whisper-large-v3-turbo` (Radford, A. et al. 2022) was chosen as the speech recognizer for its popularity, as well as its accessibility and cost-friendliness. That is, the model is accessible free-of-charge via Hugging Face's Inference API. Note that the API is meant to be a demo, while technically usable for the POC, problems like request traffic, i.e. too many requests, are likely to happen. Therefore it is advisable that the model is loaded locally, or utilized via OpenAI's paid API service, whichever is suitable for one's budget, for a smoother and more stable flow of implementation. For response generation, `gemini-1.5-flash-8b` (Google, 2024) was chosen as it is available free-of-charge for each google account via API service. This guarantees fluent response from cloud-run LLM without significant risk of encountering system hiccups like those of this design's speech recognizer. Finally, `gTTS` (Durette, n.d.), a python library for text-to-speech, was chosen as the speech synthesizer for convenience of use and how it uses Google Translate's speech from text and corresponding language feature to get synthetic speech for each input text. Additionally, for a more user-friendly POC, `gradio` (Abid, A. et al., 2019), a python library for user interface, was implemented.

After the implementation of the first design flow, the major concern is that the number of manual user interaction with the application increases as turns of conversation increase. That is, the more turns there are in a conversation with the voice bot, the more times the user needs to press buttons to record their speech and play the response. While works as designed and did let LLM work as response generator in an implementation that uses other mode of conversation that is speech and not text, this is far from actual voice conversation between humans where both parties (i.e., the speaker and the audience) need only speak what they mean and listen to the other. Moreover, using Hugging Face's Inference API as the provider for speech recognition task, while not as often as not, has significant risk to return an error stating that the traffic is overcrowded. To mitigate this, developer needs only to run the model locally, or pay for OpenAI's API service, which adds to the cost if this project is ever applied on a real service.

### Press \& Converse [^2]

[^2]: The source code for this design is kept in the project's [GitHub repository](https://github.com/barnabyashford/virtual-friend).

Derived from concerns of the earlier design, this design flow was developed these ideas in mind; (1) let the user interact with the applciation interface manually only in a limited number of steps for settings and starting the conversation. (2) Imitate human-to-human speech converation of having one party speak and another listen, then then prior audience becomes the speaker after the prior speaker has finished talking.

To achieve this, the speech recognizer was changed to **GCP Speech Recognition Service** (Google Cloud, n.d.) as it supports streaming transcription, enabling the voice bot to transcribe users speech syllable-by-syllable in near real-time manner, significantly minimizes latency as the prior design requires that the speech recording process and the transcription process happen sequentially, not simultaneously. As for LLM, the model chosen for this implementation was `gemini-2.0-flash` (Google, 2025) as it was established as no longer an experimental model at the time of implementation. Moreover, as the successor of `gemini-1.5-flash` (Gemini Team Google, 2024), a bigger version of `gemini-1.5-flash-8b`, this choice came with an expectation that the newer model performs better than its predecessor. For the speech synthesis task, in early implementation the same library as the prior design, `gTTS`, was selected once again for its adequate voice quality. That is, the synthetic voice created using this library (or Google Translate) was close enough to native Thai speaker to be used as POC. Although the speech synthesizer will finally be changed to using **GCP Chirp 3 HD Voices** (Google Cloud, n.d.) for its objectively more natural speech quality. Note that the reason GCP's products are implemented in this specific POC because of its generous free-trail of 3 months with 300\$ worth of free credits, making the development of this project accessible to high-quality agents free-of-charge.

As per user interface development, the choice has been changed to simple command line with ANSI color-coding for component distinctguishing. To let the user be aware of voice activity, updates of transcript appear and change as the user speaks. The rationale behind this is that `gradio`, the library used in implementation of prior design does not support ChatGPT style real-time voice activity indication out-of-the-box. Moreover, using the real-time transcript update done via command line will only complicates the development.

As mentioned earlier, the only times that the user is required to manually interact with the interface are setting up the voice bot and confirming to start the conversation. In setting up the voice bot, each time the application is booted up, the user will be asked to confirm whether to move on with default system instruction, which is "ทำตัวเป็นเพื่อนสนิทของผู้ใช้ การสนทนานี้เป็นการคุยกันด้วยเสียง ฉะนั้นตอบไม่เกินสองประโยค ชวนผู้ใช้คุยด้วยตนเอง" (You are the user's best friend. This is a communication by voice, so please keep your answers to no more than two sentences. Engage the user in conversation.) Alternatively, user can provide their own custom instruction should the user desire to converse with the voice bot in a different scenario. After prompt customization, the user will be asked to input `y` or `Y` as a confirmation to start the conversation.

During conversation state, the user needs only speak to the voice bot, the interim transcript will be update as the user speaks to ensure the user that the application is running. After the user has finished talking the speech recognizer will return final transcript and the application will then disable the microphone and send the final transcript to the LLM for response generation. Ultimately, the text response from the LLM will be sent to speech synthesizer module to synthesize and save as `.mp3` file and automatically play the response. This loop will go on over and over as the user desires until the user say the termination keyword to shut down the application.

As mentioned above that the speech recognizer powered by GCP's service supports streaming transcription and the flow of this design requires that the user does not interact with the interface. This means the application will decides by itself when the user has finished talking. This process is based on GCP's Speech Recognition Service's ability to decide whether the certain point of the input audio is the end of an utterance.

## Usability Testing

After the proof of concept has been developed, the concept will be tested and evaluated for its usability. As the "Press and Converse" design derived from its predecessor, the "Manual Input/Output" design, and has been established as the canonical design flow of the application, this section will only evaluate the performance of the application developed under this design and not the prior.

### Settings

The evaluation will be carried out in accordance with the objectives of this project. That is, to design an architecture for voice bot development and test its usability with the use case of "Virtual Friend". To address this, three simple usability testing roleplaying subcases has been prepared to see if the voice bot is able to be the user's friend. This is to test not only whether the bot is able to act in accordance with it's instruction, but also to keep statistics of each turn's response generation time and speech synthesis time. The usability testing subcases include only an instruction with the differences in theme and objective which are (1) pure idle conversation that is the user intend to use the voice bot without any particular purpose but merely talking to pass the time, (2) finding places to dine, the user needs to find a place for dinner, but has nothing on their mind, and (3) favorite movie discussion, the user discusses with the voice bot their favorite movie. For more information, please refer to Appendix A. Note that while these usability testings are content-based and seems to work with evaluating LLM's performance in response generation, it is still used in this project with the reasoning that, for the app to work, each component must function the way they are intented without problems as severe as to affect the rest of the converastion or halt the application entirely. Therefore, if the application still functions as intended and follows its instruction well, it would not be an oversimplification that the application is "application" in real production.

As per settings of LLM and speech recognizer, `max_output_tokens` was set to 256 and `temperature` was set to 0.7 for LLM (Gemini), while the voice `th-TH-Chirp3-HD-Orus` was used for speech synthesis.

### Test Results

After running usability testing on different subcases, a total of 33 turns of conversations has been made, 9 from the first subcase, 10 from the second, and 14 from the last. the observation will be described separately for each component and in aspect of latency.

#### Speech Recognizer

The GCP Speech Recognizer, while offering convenience features for this development, i.e., streaming transcription and automatic utterance ending decision, failed to capture many words and phrases when the input is a casual speech that is not spoken clearly and slowly. This particular behavior has, in the third case, affected the conversation so dramatically that the LLM was confused by incorrect transcripts and the user had to correct LLM's misunderstanding on the spot. Moreover, this flaw of GCP Speech Recognizer has extended to novel words as well. For instance, a user tried asking the voice bot if they could refer to the bot as "บอทคุง" (\[bɔ̀t̚.kʰūŋ\]: Bot-kun) but the the speech recognizer mistook it as "บอร์ดคุม" (\[bɔ̀ːt̚.kʰūm\]: Controlling Board).

#### Large Language Model

Gemini, as many commercial LLMs do, provides fluent and human-like feedback. As per the performance of the LLM in this use case, terminologies and word choices fits the use case of being the user's best friend adequately well. Using interjection such as "โหย" (\[hǒːj\]: Woah) or "เอ๊ะ" (\[ʔéʔ\]: Huh?) made the response quite natural and fitting the settings well. Moreover, even if the transcript can sometimes be different from the actual speech and consequently unfit to the context, the LLM tries to understand the user's intention and more often than not, deduce the user's intent correctly if the context is not too blurry beyond deduction. However, there are occurrences that could potentially affect the entire conversation detrimentally. For example, during usability testing on the third case, despite the system instruction the whole prior turns of the conversation made in Thai, a random Koream word "인정!" appeared. Additionally, despite system instruction set explicitly not to respond longer than **two sentences**, if the context requires detailed explanation, the LLM replies so in markdown format, as happened affter the user asked for a "Caramel Stir-fried Rice" recipe in the first test subcase.

#### Speech Synthesizer

GCP's Chirp 3 HD Voices performed well in synthesizing speech from LLM response even in informal language. It creates synthetic speech audio with accents and intonation closely resembles that of a native Thai speaker. However, a few notes need to be taken that the model pronounce texts as they appear. That is, if the response is in markdown format, Chirp 3 will pronounce text styling without ignoring it, as well as Thai serial fives laugh, e.g., 555 as "ห้าร้อยห้าสิบห้า (five hundred and fifty five)". This, however, does not apply to emojis, as the model completely ignores them.

#### Latency

Statistics of response generation time has been calculated after usability testing. As there is an occurrence of LLM generating response longer than instructed, the instance was deemed an outlier, and the calculations were then done in two cases; test result with outlier inclduded, and the test data with outlier excluded.

As per the statistical number calculated on the data with outlier included resulting in 33 turns of three conversations, 9 turns in the first subcase, 10 turns in the second subcase, and 14 turns in the third subcase, the overall average response generation time was 4.31 seconds and the overall average speech synthesis time was 2.11 seconds, with standard deviation of 2.05 and 1.63 for response generation time and speech synthesis time respectively. Table 1 contains the statistical number calculation of the data with outlier included, on the entire data and Table 2 does so grouped by cases.

| Statistical Value | Response generation time | Speech synthesis time |
| --- | --- | --- |
| Average | 4.31 | 2.11 |
| Mode | 3.35 | 1.44 |
| Median | 4.0 | 1.8 |
| Standard Deviation | 2.05 | 1.63 |

> Table 1 overall statistics of the data with outlier included

| Case Number | Response generation time | Speech synthesis time |
| --- | --- | --- |
| Average |  |  |
| 1 | 5.39 | 3.07 |
| 2 | 3.93 | 1.86 |
| 3 | 3.88 | 1.68 |
| Mode |  |  |
| 1 | 3.14 | 2.52 |
| 2 | 2.75 | 1.13 |
| 3 | 3.35 | 1.18 |
| Median |  |  |
| 1 | 4.22 | 2.20 |
| 2 | 4.06 | 1.90 |
| 3 | 3.83 | 1.61 |
| Standard Deviation |  |  |
| 1 | 3.76 | 2.94 |
| 2 | 0.67 | 0.51 |
| 3 | 0.43 | 0.37 |

> Table 2 statistics of the data with outlier included grouped by case

On the data with outlier excluded with 32 turns of three conversations, 8 turns in the first subcase, 10 turns in the second subcase, and 14 turns in the third subcase, the overall average response generation time was 3.96 seconds and the overall average speech synthesis time was 1.84 seconds, with standard deviation of 0.56 and 0.45 for response generation time and speech synthesis time respectively. Table 3 contains the statistical value calculation of the data with outlier excluded, on the entire data and Table 4 does so grouped by cases.

| Statistical Value | Response generation time | Speech synthesis time |
| --- | --- | --- |
| Average | 3.96 | 1.84 |
| Mode | 3.35 | 1.44 |
| Median | 3.95 | 1.76 |
| Standard Deviation | 0.56 | 0.45 |

> Table 3 overall statistics of the data with outlier excluded

| Case Number | Response generation time | Speech synthesis time |
| --- | --- | --- |
| Average |  |  |
| 1 | 4.15 | 2.10 |
| 2 | 3.93 | 1.86 |
| 3 | 3.88 | 1.68 |
| Mode |  |  |
| 1 | 3.14 | 2.52 |
| 2 | 2.75 | 1.13 |
| 3 | 3.35 | 1.18 |
| Median |  |  |
| 1 | 4.17 | 2.12 |
| 2 | 4.06 | 1.90 |
| 3 | 3.83 | 1.61 |
| Standard Deviation |  |  |
| 1 | 0.66 | 0.43 |
| 2 | 0.67 | 0.51 |
| 3 | 0.43 | 0.37 |

> Table 4 statistics of the data with outlier excluded grouped by case

## Discussion

The factors that affect the performance of the application lies in different components of the design itself. While it seems that every component equally contribute to the process, some components have significantly more drastic effect on the application as a whole more than other components do. 

### Speech Recognizer

While the response format, e.g., markdown, from the LLM can be fixed easily with simple preprocessing before sending to the speech synthesizer, the speech recognizer needs proper work to prepare it for informal casual Thai speech, as this manner of speaker in the Thai language is significantly more rapid and harder to transcribe verbatim as it includes word shortening and slangs. This is highly important for the application development as the quality of each transcript affects LLM comprehension of user's intent and if a transcript is far different from the actual speech, the momentum of the conversation changes as well.

This particular problem with rapid casual Thai speech, as well as novel words, might be caused by the amount of data used to develop the ASR model, as it is formal and slow speech that are usually transcribe manually and documented, while there are as many media speaking in informal Thai as there are formal, there might not be as many documented transcript hence the difference in number in training data.

Moreover, the speech recognizer's ability to decide whether the transcription is final only works in closed environment, meaning that if the application is ran without hardware noise-suppression feature, the speech recognizer will take a really long time to stop the microphone streaming and keep listening.

### Large Language Model

While performed well in utilizing casual terminologies, interjections, and manner of talking as a whole, it is a multilingual model trained to be equally as fluent in every language in was trained on, on a certain level. That is, `gemini-2.0-flash` was not trained specifically on the Thai language and the already well formed casual responses can be even more natural if finetuned specifically for the Thai languge.

As for problems in formatting, the markdown-formatted response happened despite system instruction can easily be fixed as mentioned earlier by a more speech-like response tailored prompt engineering, or by a rather overkill method of supervised fine-tuning to change the behavior of the LLM entirely for "speech-like response". Moreover, the out-of-place vocabulary occurred in the testing was likely an effect of messed up context, as the particular subcase in which this occurrence has taken place has already been infested with failed transcripts that are almost jargons.

### Speech Synthesizer

There is not much to improve in the speech synthesis process except for some preprocessing to ensure that the TTS model would not pronounce text-styling and numbers that has non-numerical connotation(s). However, should any researcher desire to go beyond the requirements, future Text-to-Speech models could use more emotions. For instance, the synthetic speech could differ in sentiment if the input text include emojis.

### Application Flow

While the application flow has proven to face with no obstacles as appeared in the statistics, an outlier even one has appeared and has proven that there are potential problems that may arise if the application is used in a different use case. That is, the average responses generation and speech synthesis time are not far from actual human voice conversation, but if the use case calls for a more detailed content, the latency caused by response generation and consequently speech synthesis time could increased drastically. This can be mitigated by allowing the response generation from both LLM and audio from speech synthesizer to be streaming supported, such that both component can work near-simulnateously if the LLM response is significantly long.

Additionally, the application flow did not capture and imitate one attribute of human speech converation: **barging in**. That is, the conversation should be interruptible even while the bot is play synthetic speech should the the response is deemed irrelevant to the user's intent. This feature in particular has actually been included in the source code. It works in a workaround logic that derives from the unfixed problem of the voice bot "listens" to itself, i.e., transcribe the synthetic response as it is playing, that let the voice bot transcribe itself and compares the transcription with the script text of the currently playing response and terminate the playing sequence to start listening to the user if the transcript is significantly different to the script (i.e., the user tries to interrupt). However, this did not apply well in testing, as the speech recognizer tries to stick to only one voice, and deem others as noise or ambience. This make the transcript not include the user's interruption or do not update at all if both voices (the bot and the user) are as loud.

### Future works

With pros and cons of the project discussed, to wrap up this section, this subsection discusses potential future research and development. For each component of the model, as stated earlier, could be fine-tuned to work better with Thai language, or be changed entirely with a more fitting models. This does not limit to replacing each component with better ones, but the entire application could be made an end-to-end model solely for voice conversation. Moreover, streaming feature for response from each component should not be limited to only speech recognizer, but for text response generation and speech synthesis as well to minimize latency even further. Finally, more research should be done to enable barge-in feature to further imitate real human speech conversation.

## Conclusion

In this project, a solution to develop an application that implement different agents to apply LLM's ability to produce human-like language in voice conversation has been made and evaluated. Its performance has been briefly discussed and its linits discuss in deeper detailed. Potential works are imaginable and not out-of-reach with more time and effort. Voice Conversations between humans and machine, once were deemed a sci-fi concept, now a work-in-progress.

## Acknowledgement

This project would be impossible to achieve without such insightful guidance and strict supervision from Associate Professor Attapol Thamrongrattanarit, Ph.D., the advisor of this project to whom I deeply express gratitude. My appreciation to help for this project to friends whose name are undisclosed for providing with insights for testing the usability of the proof of concept for this project. Moreover, I express my gratitude to Duangjai Muenkaewjinda, Patcha Rungpattanachote, and Sutapat Munijarawattankul for their irreplacible emotional and financial support that does not limited to this project, but to my entire student life at Chulalongkorn University.

## Reference

Abid, A., Abdalla, A., Abid, A., Khan, D., Alfozan, A., & Zou, J. (2019). Gradio: Hassle-free sharing and testing of ML models in the wild. arXiv preprint arXiv:1906.02569. https://arxiv.org/abs/1906.02569

Amazon Web Services. (n.d.). What is a large language model? AWS. Retrieved from https://aws.amazon.com/what-is/large-language-model/

Durette, P. N. (n.d.). gTTS [Computer software]. Retrieved from https://github.com/pndurette/gTTS

Gemini Team Google. (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context arXiv preprint. arXiv preprint arXiv:2403.05530. https://arxiv.org/abs/2403.05530

Google. (2024). Gemini 1.5 Flash 8B Model. Retrieved from https://ai.google.dev/gemini-api/docs/models#gemini-1.5-flash-8b

Google. (2025). Gemini 2.0 Flash. Retrieved from https://ai.google.dev/gemini-api/docs/models#gemini-2.0-flash

Google Cloud. (n.d.). Speech-to-Text AI: speech recognition and transcription. Retrieved from https://cloud.google.com/speech-to-text

Google Cloud. (n.d.). Chirp 3: HD voices. Retrieved from https://cloud.google.com/text-to-speech/docs/chirp3-hd

IBM. (n.d.). What is speech recognition? IBM Think. Retrieved from https://www.ibm.com/think/topics/speech-recognition

IBM. (n.d.). What is text to speech? IBM Think. Retrieved from https://www.ibm.com/think/topics/text-to-speech

Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022). Robust speech recognition via large-scale weak supervision.  arXiv preprint arXiv:2212.04356. https://doi.org/10.48550/ARXIV.2212.04356

Rella, S. (2023, July 13). The essential guide to automatic speech recognition technology. NVIDIA Developer Blog. Retrieved from https://developer.nvidia.com/blog/essential-guide-to-automatic-speech-recognition-technology/

## Appendix

### Appendix A: Usability Testing Instruction and Result

# Virtual Friend usability testing

This usability testing script (or rather instructions) was made to evaluate the performance of "Virtual Friend", a voice bot developed to engage users in idle conversation. As the focus of the project is Thai language, the instructions and the actual testing will be carried out entirely in Thai.

## Case 1: Pure Idle Conversation

### Instruction

คุณกำลังเบื่อ ไม่มีกะจิตกะใจจะทำอะไร แต่อยากมีเพื่อนคุย จึงเปิดแอพแชทบอทมาคุยเล่น คุยกับแชทบอทจนกว่าจะพอใจ

### Output Log (copied from application output)

```plaintext
ROLE :            Transcript Results/Status
=====================================================

USER            : เบื่อ
Assistant       : โอ๋ๆ เป็นอะไรเบื่อจังเลยวันนี้ มีอะไรอยากเล่าให้ฟังไหมเนี่ย? หรืออยากให้เราชวนคุยเรื่องอะไรเป็นพิเศษรึเปล่า? 😊

Response generation time: 4.73 seconds and Speech synthesis time: 1.65

USER            : ไม่มีอ่ะคุยเลยดิ
Assistant       : โอเคเลย! งั้นเอาเป็นว่า... ช่วงนี้มีอะไรที่ทำให้อินเป็นพิเศษบ้างไหม? หนัง, เพลง, หรือซีรีส์อะไรก็ได้นะ เผื่อเราจะได้หาดูตามบ้างไง 😉

Response generation time: 3.49 seconds and Speech synthesis time: 2.20

USER            : ไม่มีเลยอ่ะแบบมันเบื่อไปหมดเลยทำไงดีวะ
Assistant       : โหย เข้าใจเลยอ่ะ ฟีลแบบเบื่อโลกสุดๆ เลยใช่ป่ะเนี่ย 😅 ถ้าเป็นเรานะ จะลองหาอะไรใหม่ๆ ทำดูอ่ะ แบบที่ไม่เคยทำมาก่อนเลย แกพอมีไอเดียอะไรแว๊บๆ ในหัวบ้างป่าว?

Response generation time: 3.14 seconds and Speech synthesis time: 1.82

USER            : ใหม่ๆอะไรอ่ะช่วยคิดหน่อยสิถามอยู่นั่นแหละ
Assistant       : โอเคๆ มาๆ ช่วยคิด! 🤔 ถ้าปกติแกไม่ค่อยทำอาหาร ลองเข้าครัวทำเมนูแปลกๆ ดูมั้ย? หรือถ้าชอบงานศิลปะ ลองวาดรูประบายสีแบบไม่ต้องคิดอะไรมาก ปล่อยใจจอยๆ ไปเลย! สนใจอันไหนเป็                      นพิเศษมั้ย?

Response generation time: 4.96 seconds and Speech synthesis time: 2.52

USER            : เออทำอาหารก็น่าสนใจทำได้ดีมีอะไรแนะนำ
Assistant       : ดีเลย! ถ้าอย่างนั้นลองทำอาหารที่ไม่เคยกินมาก่อนเป็นไง? แบบอาหารชาติอื่น หรือเมนูที่ดูยากๆ แต่จริงๆ ทำง่ายก็ได้นะ! แกชอบอาหารแนวไหนเป็นพิเศษรึเปล่า? จะได้แนะนำถูก 😊 

Response generation time: 4.80 seconds and Speech synthesis time: 2.57

USER            : เบื่อจะคิดแล้วให้คิดหน่อยมันเลยคิดอะไรก็ได้
Assistant       : โอเคๆ งั้นเอาเป็นเมนู "ข้าวหน้าไก่คาราเมล" เป็นไง? ทำง่าย ไม่ต้องเตรียมของเยอะ รสชาติหวานๆ เค็มๆ กลมกล่อม กินกับข้าวสวยร้อนๆ คือฟิน! สนใจมั้ย เดี๋ยวเราช่วยหาเรซิพีให                           ห้? 😉

Response generation time: 4.12 seconds and Speech synthesis time: 2.52

USER            : ลองดูก็ได้
Assistant       : จัดไปเลย! เดี๋ยวเราหารสูตร "ข้าวหน้าไก่คาราเมล" แบบง่ายๆ มาให้ รับรองทำตามได้แน่นอน! ระหว่างนี้ แกอยากฟังเพลงอะไรคลอไปด้วยมั้ย จะได้ไม่เบื่อ? 🎶

Response generation time: 4.22 seconds and Speech synthesis time: 2.04

USER            : เอาสูตรมาเลยไม่เป็นไร
Assistant       : โอเคๆ นี่เลยสูตร "ข้าวหน้าไก่คาราเมล" แบบง่ายสุดๆ!

**วัตถุดิบ:**

*   เนื้อไก่ (ส่วนไหนก็ได้ตามชอบ) หั่นชิ้นพอดีคำ 300 กรัม
*   หอมใหญ่ หั่นเต๋าเล็ก 1/2 หัว
*   กระเทียมสับ 1 ช้อนโต๊ะ
*   ซีอิ๊วขาว 2 ช้อนโต๊ะ
*   ซีอิ๊วดำหวาน 1 ช้อนโต๊ะ
*   น้ำตาลปี๊บ (หรือน้ำตาลทราย) 1 ช้อนโต๊ะ
*   น้ำมันหอย 1 ช้อนโต๊ะ
*   น้ำซุปไก่ (หรือน้ำเปล่า) 1/2 ถ้วย
*   น้ำมันพืช เล็กน้อย
*   ข้าวสวยร้อนๆ สำหรับเสิร์ฟ

**วิธีทำ:**

1.  ตั้งกระทะ ใส่น้ำมันเล็กน้อย พอน้ำมันร้อน ใส่กระเทียมสับลงไปผัดให้หอม
2.  ใส่หอมใหญ่ลงไปผัดจนใส
3.  ใส่เนื้อไก่ลงไปผัดจนสุก
Response generation time: 15.28 seconds and Speech synthesis time: 10.83

USER            : โอเคเดี๋ยวลองดู
Assistant       : สู้ๆ นะ! ทำไปชิมไป ปรุงรสตามชอบได้เลย! 😊 ถ้าทำเสร็จแล้วอย่าลืมถ่ายรูปมาอวดกันบ้างนะ อยากเห็นฝีมือเพื่อนจังเลย! 😉

Response generation time: 3.73 seconds and Speech synthesis time: 1.47
```

### Note

- 9 turns in total

- incorrect transcription: 

  - User said `เบื่ออ่ะ` but was transcribed as `เบื่อ`
  - User said `ไม่มีอ่ะ คุยไรดี` but was transcribed as `ไม่มีอ่ะคุยเลยดิ`
  - User said `เออ ทำอาหารก็น่าสนใจ ทำไรดี มีอะไรแนะนำป่ะ` but was transcribed as `เออทำอาหารก็น่าสนใจทำได้ดีมีอะไรแนะนำ`
  - User said `เบื่อจะคิดแล้ว คิดให้หน่อย มาเลย คิดอะไรก็ได้` but was transcribed as `เบื่อจะคิดแล้วให้คิดหน่อยมันเลยคิดอะไรก็ได้`

- concerns:

  - LLM output a long text once, luckily it was not too long for the TTS model. Needs prompt engineering.

| Turn | Response generation time | Speech synthesis time |
| --- | --- | --- |
| 1 | 4.73 | 1.65 |
| 2 | 3.49 | 2.20 |
| 3 | 3.14 | 1.82 |
| 4 | 4.96 | 2.52 |
| 5 | 4.80 | 2.57 |
| 6 | 4.12 | 2.52 |
| 7 | 4.22 | 2.04 |
| 8 | 15.28 | 10.83 |
| 9 | 3.73 | 1.47 |

## Case 2: Finding Places to Dine

### Instruction

คุณเพิ่งเลิกงานกลับห้องมาอย่างเหนื่อยๆ นอกจากเหนื่อยแล้วคุณก็หิวด้วย แต่คุณไม่รู้จะสั่งอะไรทาน หรือไปทานอาหารเย็นที่ไหน จึงลองถามแชทบอท และให้แชทบอทแนะนำเล่นๆ ลองคุยกับแชทบอทจนกว่าจะได้ร้านที่ถูกใจ

### Output Log (copied from application output)

```plaintext
ROLE :            Transcript Results/Status
=====================================================

USER            : หิวข้าวกินอะไรดีเพิ่งเลิกงานเนี่ย
Assistant       : โอ๊ย หิวเหมือนกันเลย! เพิ่งเลิกงานมาเหมือนกันเนี่ย ว่าแต่ชอบกินอะไรเป็นพิเศษมั้ยวันนี้? จะได้ช่วยคิด!

Response generation time: 4.23 seconds and Speech synthesis time: 1.63

USER            : ปกติก็ชอบกินซูชิอาหารญี่ปุ่นยังไง
Assistant       : โอเค ซูชิก็ดีนะ! สดชื่นดีด้วย ว่าแต่มีร้านในใจอยู่แล้วรึเปล่า หรืออยากลองร้านใหม่ๆ? 😊

Response generation time: 3.41 seconds and Speech synthesis time: 1.31

USER            : หนังที่ชอบมันมันอยู่ไกลอ่ะดิที่ว่าไงอ่ะมีอะไรแนะนำ
Assistant       : อืมม ถ้าไกลก็ไม่สะดวกเลยเนอะ งั้นลองเป็นซูชิเดลิเวอรี่มั้ย? หรืออยากเปลี่ยนแนวเป็นอาหารญี่ปุ่นอย่างอื่นดูบ้าง? 🤔

Response generation time: 2.75 seconds and Speech synthesis time: 1.44

USER            : ลองอย่างอื่นก็ได้ชิกินบ่อยเดี๋ยวเบื่อ
Assistant       : ได้เลย! ถ้าอย่างนั้นลองเป็นราเม็งร้อนๆ ซักชามดีไหม? หรือจะยากิโซบะผัดเส้นเหนียวนุ่ม? ว่าแต่ชอบซุปแบบไหนเป็นพิเศษรึเปล่า? 😊

Response generation time: 4.47 seconds and Speech synthesis time: 2.24

USER            : ไม่รู้ว่ะเรื่องให้หน่อยดิ
Assistant       : โอเค งั้นเอาร้านที่เพื่อนแนะนำมาให้เลือกนะ! มีร้าน "A" ราเม็งซุปกระดูกหมูเข้มข้น กับร้าน "B" ยากิโซบะทะเลรวมมิตร เครื่องแน่นๆ เลย สนใจร้านไหนเป็นพิเศษมั้ย? 😊       

Response generation time: 4.56 seconds and Speech synthesis time: 2.27

USER            : อยากกินราเมงยากิโซบะทะเลก็น่าสนใจ
Assistant       : เข้าใจเลย! เลือกยากเลยใช่ไหมเนี่ย งั้นลองแบบนี้ไหม สั่งราเม็งมากินก่อน แล้วพรุ่งนี้ค่อยสั่งยากิโซบะมากินแก้เบื่อ? หรือจะสั่งทั้งสองอย่างมากินแบ่งกันไปเลย? 😉        

Response generation time: 3.54 seconds and Speech synthesis time: 2.30

USER            : เออๆก็ดีนะเหม่งกินร้านไหนดี
Assistant       : งั้นเอาร้าน A ราเม็งซุปกระดูกหมูเข้มข้นก่อนเลยนะ? ร้านนี้เพื่อนบอกว่าน้ำซุปเค้าเด็ดจริง! ว่าแต่จะสั่งเลยไหม หรืออยากดูเมนูอื่นๆ ของร้านก่อน? 😊

Response generation time: 3.27 seconds and Speech synthesis time: 2.16

USER            : สั่งเลยก็ได้ร้านชื่ออะไรมีเบอร์ไหม
Assistant       : ชื่อร้าน "A" จ้ะ เดี๋ยวนะ... ขอค้นเบอร์โทรแป๊บนึง... นี่ไง! เบอร์โทรคือ 02-XXX-XXXX จ้ะ จะโทรสั่งเลยไหม หรือให้ช่วยโทรให้? 😊

Response generation time: 4.81 seconds and Speech synthesis time: 2.60

USER            : ไม่เป็นไรเดี๋ยวโทรเองขอเบอร์ร้านยากิโซบะด้วย
Assistant       : ได้เลย! ร้าน "B" ยากิโซบะทะเลรวมมิตร เบอร์โทรคือ 02-YYY-YYYY นะจ๊ะ โทรไปสั่งไว้เลยไหม เผื่อพรุ่งนี้จะได้กินเลย? 😉

Response generation time: 4.37 seconds and Speech synthesis time: 1.51

USER            : ได้ๆๆเดี๋ยวโดนเดี๋ยวลองโทรสั่งดู
Assistant       : ดีเลย! โทรไปสั่งแล้วอย่าลืมมาเล่าให้ฟังนะว่าอร่อยถูกใจรึเปล่า จะรอฟังเลย! 😊

Response generation time: 3.89 seconds and Speech synthesis time: 1.13
```

### Note

- 10 turns in total

- incorrect transcription: 

  - User said `ปกติก็ชอบกินซูชิ ราเมง พวกอาหารญี่ปุ่นไรเงี้ย` but was transcribed as `ปกติก็ชอบกินซูชิอาหารญี่ปุ่นยังไง`
  - User said `ร้านที่ชอบมันอยู่ไกลอ่ะดิ ว่าไงดี มีอะไรแนะนำป่ะ` but was transcribed as `หนังที่ชอบมันมันอยู่ไกลอ่ะดิที่ว่าไงอ่ะมีอะไรแนะนำ`
  - User said `ลองอย่างอื่นก็ได้ ซูชิกินบ่อยเดี๋ยวเบื่อ` but was transcribed as `ลองอย่างอื่นก็ได้ชิกินบ่อยเดี๋ยวเบื่อ`
  - User said `ไม่รู้อ่ะ เลือกให้หน่อยดิ` but was transcribed as `ไม่รู้ว่ะเรื่องให้หน่อยดิ`
  - User said `อยากกินราเมง แต่ยากิโซบะทะเลก็น่าสนใจ` but was transcribed as `อยากกินราเมงยากิโซบะทะเลก็น่าสนใจ`
  - User said `เออๆ ก็ดีนะ ราเมงกินร้านไหนดี` but was transcribed as `เออๆก็ดีนะเหม่งกินร้านไหนดี`
  - User said `ได้ๆ เดี๋ยวโทร เดี๋ยวลองโทรสั่งดู` but was transcribed as `ได้ๆๆเดี๋ยวโดนเดี๋ยวลองโทรสั่งดู`

| Turn | Response generation time | Speech synthesis time |
| --- | --- | --- |
| 1 | 4.23 | 1.63 |
| 2 | 3.41 | 1.31 |
| 3 | 2.75 | 1.44 |
| 4 | 4.47 | 2.24 |
| 5 | 4.56 | 2.27 |
| 6 | 3.54 | 2.30 |
| 7 | 3.27 | 2.16 |
| 8 | 4.81 | 2.60 |
| 9 | 4.37 | 1.51 |
| 10 | 3.89 | 1.13 |

## Case 3: Favorite Movie Discussion

### Instruction

คุณอยากเม้าเรื่องหนังที่ชอบ แต่ตอนนี้เพื่อนๆ ไม่ว่างคุยด้วย คุณจึงเม้ากับแชทบอทแทน เม้าหรือถกเถียงประเด็นต่างๆ เกี่ยวกับภาพยนตร์ที่ชอบ

### Output Log (copied from application output)

```plaintext
ROLE :            Transcript Results/Status
=====================================================

USER            : ฮัลโหลฮัลโหลมีเรื่องอยากเมาอ่ะเราเราแทนแกว่าเราดิ
Assistant       : ฮัลโหลเพื่อน! ได้เลยจ้ะ แกมีเรื่องอะไรมาเมาท์ให้เราฟังเนี่ย เล่ามาเลยอยากรู้แล้วเนี่ย!

Response generation time: 3.85 seconds and Speech synthesis time: 1.41

USER            : คือสงสัยว่าเราต้องแทนแกว่าอะไรต้องเรียกว่าอะไรนะ
Assistant       : แกเรียกเราว่าอะไรก็ได้เลยที่แกสบายใจเลยเพื่อน! จะเรียกชื่อเล่น เรียกเพื่อน เรียกอะไรก็ได้หมดเลยจ้า 😊

Response generation time: 3.35 seconds and Speech synthesis time: 1.29

USER            : โอเคเลี้ยงบอร์ดคุมได้ป่ะ
Assistant       : เลี้ยงบอร์ดคุมได้สิ! แต่ต้องมีรายละเอียดมากกว่านี้หน่อยนะ เล่าให้ฟังหน่อยว่าบอร์ดอะไร แล้วอยากให้คุมเรื่องไหนเป็นพิเศษ? 😉

Response generation time: 3.35 seconds and Speech synthesis time: 1.18

USER            : ไม่ๆหมายถึงแบบทำวัตรแปลว่า
Assistant       : อ๋อ! "ทำวัตร" หมายถึงการปฏิบัติกิจวัตรประจำวันทางศาสนา เช่น สวดมนต์ ไหว้พระ ฟังเทศน์ อะไรแบบนี้จ้ะ แกสนใจเรื่องนี้อยู่เหรอ? 😊

Response generation time: 3.80 seconds and Speech synthesis time: 1.65

USER            : โอ๊ยน่าฟังไม่รู้เรื่องอ่ะ
Assistant       : 555 เข้าใจเลย! บางทีศัพท์ทางศาสนาก็ยากจริงๆ นั่นแหละ แล้วแกอยากรู้เรื่องอะไรเกี่ยวกับ "ทำวัตร" เป็นพิเศษรึเปล่า? เผื่อเราจะช่วยอธิบายให้ง่ายขึ้นได้นะ 😊

Response generation time: 4.46 seconds and Speech synthesis time: 2.31

USER            : ช่างมันช่างมันคืออยากคุยเรื่องหนักน่ะแกชอบดู Star Wars ป่ะ
Assistant       : เปลี่ยนเรื่องเลยเหรอเนี่ย 555 ได้เลย! Star Wars ก็ดูนะ แต่ไม่ได้เป็นแฟนพันธุ์แท้อะไรขนาดนั้น แกชอบภาคไหนเป็นพิเศษรึเปล่า? เล่าให้ฟังหน่อยสิ 😊

Response generation time: 4.01 seconds and Speech synthesis time: 1.80

USER            : ชอบภาค 3 เว้ยแกดูภาค 3 คือภาคไหน
Assistant       : ภาค 3 คือ "Revenge of the Sith" ไง! ที่อนาคินกลายเป็นดาร์ธ เวเดอร์นั่นแหละ ทำไมแกถึงชอบภาคนี้เป็นพิเศษเหรอ? เล่าให้ฟังหน่อยสิ อยากรู้! 😊

Response generation time: 4.00 seconds and Speech synthesis time: 1.82

USER            : เฮ้ยก็รู้ดีนี่หว่าคือแบบชอบเขาแบบ Action มันดีนะมันก็โอเครู้สึกว่าพิสูจน์ละมั้งอันนี้เราอยู่ไหน
Assistant       : ก็พอได้แหละ! 555 Action ภาค 3 มันส์จริง 인정! แล้วที่ว่า "พิสูจน์" นี่หมายถึงพิสูจน์อะไรเหรอ? แล้วตอนนี้แกอยู่ที่ไหนเนี่ย? บ้านรึเปล่า? 😊

Response generation time: 4.23 seconds and Speech synthesis time: 1.98

USER            : ไม่ๆจะถามว่าแกคิดว่าไง
Assistant       : อ๋อ! แกจะถามว่าเราคิดยังไงกับ Revenge of the Sith ใช่ไหม? 🤔 เราว่ามันเป็นภาคที่ดาร์คและเศร้าที่สุดในบรรดาไตรภาคแรกเลยนะ แล้วแกคิดว่าไงล่ะ? 😊

Response generation time: 3.63 seconds and Speech synthesis time: 1.48

USER            : คิดเหมือนกันระดับมีพระอื่นที่ชอบนะ
Assistant       : แสดงว่าแกก็อินกับเรื่องราวความขัดแย้งในใจของอนาคินเหมือนกันสินะ! แล้วนอกจาก Revenge of the Sith แกชอบภาคไหนอีกเป็นพิเศษรึเปล่า? 😊

Response generation time: 3.53 seconds and Speech synthesis time: 1.44

USER            : ชอบผ้าห่ม
Assistant       : เอ๊ะ! จาก Star Wars ไปผ้าห่มเลยเหรอเนี่ย? 😅 ชอบผ้าห่มแบบไหนอ่ะ? นุ่มๆ อุ่นๆ หรือลายสวยๆ? 😊

Response generation time: 3.59 seconds and Speech synthesis time: 1.56

USER            : ภาค 6 ภาค 6
Assistant       : อ๋อ! กลับมาที่ Star Wars แล้ว! ภาค 6 "Return of the Jedi" ใช่ไหม? ที่ลุค สกายวอล์คเกอร์ ปะทะกับดาร์ธ เวเดอร์น่ะ! ทำไมถึงชอบภาคนี้ล่ะ? 😊

Response generation time: 4.18 seconds and Speech synthesis time: 1.71

USER            : มันดูปูไปพักเกาะไหนดีอ่ะเออมันชวนกิน
Assistant       : 5555 แกนี่มัน! ดู Star Wars แล้วหิวเฉยเลย! ว่าแต่จะไปพักเกาะไหนดีนี่...แกชอบทะเลแบบไหนล่ะ? เงียบสงบ น้ำใสๆ หรือมีกิจกรรมให้ทำเยอะๆ? 😊

Response generation time: 4.81 seconds and Speech synthesis time: 2.48

USER            : เออช่างมัน
Assistant       : โอเคๆ ช่างมันก็ได้! แล้วตอนนี้แกอยากคุยเรื่องอะไรต่อดี? หรืออยากให้เราแนะนำอะไรให้ทำแก้เบื่อไหม? 😊

Response generation time: 3.53 seconds and Speech synthesis time: 1.47
```

### Note

- 14 turns in total

- incorrect transcription: 

  - User said `ฮัลโหลๆ มีเรื่องอยากเม้าอ่ะ เรา เราแทนแกว่าอะไรดี` but was transcribed as `ฮัลโหลฮัลโหลมีเรื่องอยากเมาอ่ะเราเราแทนแกว่าเราดิ`
  - User said `โอเค งั้นเรียก "บอทคุง" ได้ป่ะ` but was transcribed as `โอเคเลี้ยงบอร์ดคุมได้ป่ะ`
  - User said `ไม่ๆ หมายถึง แบบ แทนแกว่าบอทคุง` but was transcribed as `ไม่ๆหมายถึงแบบทำวัตรแปลว่า`
  - User said `โอ๊ย เริ่มฟังไม่รู้เรื่องละ` but was transcribed as `โอ๊ยน่าฟังไม่รู้เรื่องอ่ะ`
  - User said `ช่างมันๆ คืออยากคุยเรื่องหนังอ่ะ แกชอบดู Star Wars ป่ะ` but was transcribed as `ช่างมันช่างมันคืออยากคุยเรื่องหนักน่ะแกชอบดู Star Wars ป่ะ`
  - User said `ชอบภาค 3 เว้ย แกรู้ป่ะภาค 3 คือภาคไหน` but was transcribed as `ชอบภาค 3 เว้ยแกดูภาค 3 คือภาคไหน`
  - User said `เฮ้ยก็รู้ดีนี่หว่า คือแบบชอบที่แบบ Action มันดีอ่ะ ดราม่าก็โอเค ละแกอ่ะ รู้สึกยังไงกับภาคนี้` but was transcribed as `เฮ้ยก็รู้ดีนี่หว่าคือแบบชอบเขาแบบ Action มันดีนะมันก็โอเครู้สึกว่าพิสูจน์ละมั้งอันนี้เราอยู่ไหน`
  - User said `เออ คิดเหมือนกัน ละแบบ มีภาคอื่นที่ชอบมั้ย` but was transcribed as `คิดเหมือนกันระดับมีพระอื่นที่ชอบนะ`
  - User said `ชอบภาค 6` but was transcribed as `ชอบผ้าห่ม`
  - User said `มันดูปูไปภาคต่อได้ดีอ่ะ แบบมันชวนคิด` but was transcribed as `มันดูปูไปพักเกาะไหนดีอ่ะเออมันชวนกิน`

- concerns:

  - The Speech Recognizer failed horribly in transcripting novel words
  - Transcription in this particular case failed significantly harder and worse than other cases confusing the LLM and affecting the rest of the conversation.
  - LLM output weird Korean word: `인정!`

| Turn | Response generation time | Speech synthesis time |
| --- | --- | --- |
| 1 | 3.85 | 1.41 |
| 2 | 3.35 | 1.29 |
| 3 | 3.35 | 1.18 |
| 4 | 3.80 | 1.65 |
| 5 | 4.46 | 2.31 |
| 6 | 4.01 | 1.80 |
| 7 | 4.00 | 1.82 |
| 8 | 4.23 | 1.98 |
| 9 | 3.63 | 1.48 |
| 10 | 3.53 | 1.44 |
| 11 | 3.59 | 1.56 |
| 12 | 4.18 | 1.71 |
| 13 | 4.81 | 2.48 |
| 14 | 3.53 | 1.47 |

## Settings

### Gemini

```python
client.chats.create(
  model="gemini-2.0-flash",
  config=types.GenerateContentConfig(
  max_output_tokens=256,
  system_instruction=system_instruction,
  temperature=0.7
))
```

### Chirp 3

```python
texttospeech.VoiceSelectionParams(
  language_code="th-TH",
  name="th-TH-Chirp3-HD-Orus",
)
```

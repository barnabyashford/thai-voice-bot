> A repository for....

# Thai Voice-based Virtual Friend

A voice bot application developed as a part of **2209492 Project in Language Technology II** course of the Faculty of Arts, Chulalongkorn University. This application allows you to have a friendly and casual conversation on plethora of topics. The "Bot" acts as your best friends who is always down to keep you occupied, or better yet, help you with decisions where you simply need a second opinion.

## Getting Started

### Setting Up Environment

First of all, please create a directory, then, on your command line, run this command:

```cmd
cd path_to_your_directory
```

Then, clone this repository:

```cmd
git clone https://github.com/barnabyashford/virtual-friend
```

After you have finished cloning this repository, we can start setting up the virtual environment to run this application. 

```cmd
cd virtual-friend
```

After changing the working directory to `virtual-friend`, run the following command. It creates a virtual environment.

```cmd
python -m venv .venv
```

Finally, run this command. It installs the library required to run this application.

```cmd
pip install -r requirement.txt
```

### Setting Up Google Credentials

Three main components of this project implemented Google's services: [**GCP Cloud Speech-to-Text**](https://cloud.google.com/speech-to-text?_gl=1*1omcoqh*_up*MQ..&gclid=Cj0KCQjwlYHBBhD9ARIsALRu09qkdLMoiFxqejn-nxyU-UXnuH6kno1G66Keaxv_QQIztr6PKkd579YaAjxpEALw_wcB&gclsrc=aw.ds&hl=en), [**Gemini**](https://deepmind.google/technologies/gemini/), and [**GCP Chirp 3: HD Voices**](https://cloud.google.com/text-to-speech?_gl=1*1sc5veb*_up*MQ..&gclid=Cj0KCQjwlYHBBhD9ARIsALRu09qkdLMoiFxqejn-nxyU-UXnuH6kno1G66Keaxv_QQIztr6PKkd579YaAjxpEALw_wcB&gclsrc=aw.ds&hl=en). In order to run this application, you first need to set up a few credentials. Please follow these steps.

#### Google Cloud Console Credentials

Two services provided by Google Cloud Console were implemented in this project. Here is the guide for gaining access to such services:

1. Go to [GCP's main page](https://cloud.google.com/). Create an account if you haven't got one already or go to [console](console.cloud.google.com) if you have an account.
2. Create a new project.
3. From **Navigation menu** (three stripes on top left, under the Google Console logo), go to **APIs \& Services** > **Library** and search `Cloud Speech-to-Text API`.
4. Click **Enable**
5. Repeat step 3 and 4 with search keyword of `Cloud Text-to-Speech API`.
6. From **Navigation menu**, go to **IAM \& Admin** > **Service Accounts** and click "Create service account".
7. Give it a name then click **Create and continue**, then click **Done**. This will automatically take you back to the **Service Accounts** page earlier.
8. In the **Actions**, click the vertical three dots icon, then select **Manage keys**.
9. Click **Add key** dropdown, then select **Create new key**.
10. Select the key type as JSON, then click **Create**. The JSON file will automatically be downloaded to your device.
11. (optional) move the JSON into the `virtual-friend` directory.

#### Gemini API Key

This project relies on Gemini, specifically `gemini-2.0-flash` to generate response to the user's input. To use Gemini's inference API, we need to create an API key.

1. Go to [Google AI Studio](aistudio.google.com), log in with your google account, or create a new one.
2. Click **Get API key**, then click **Create API key**.
3. A window will appear where you are requested to select a Google cloud project for this specific API. You can use the same project as created earlier. Click **Create API key in existing project** to continue.
4. Copy the API key, keep it somewhere secured.

### Finishing Touch

Finally, in the `virtual-friend` directory, create a file named exactly `.env` and input this:

```plaintext
GOOGLE_APPLICATION_CREDENTIALS=<path_to_gcp_service_account_json>
GOOGLE_API_KEY="<your_gemini_api_key>"
```

## Moshi Moshi?

With eveything set, you can start using the application. Please follow these steps:

1. Activate the virtual environment created earlier using this command:

   ```cmd
   .venv\Scripts\activate
   ```
   
2. Run the python `main.py` script, this is where the application starts.

   ```cmd
   python main.py
   ```

3. The application will ask whether you want to proceed with your own custom system instruction (an instruction to the LLM, tells it what to keep in mind during the conversation with you).

   ```plaintext
   =====================================================
   Voice Bot Application
   =====================================================
   Here's the default prompt for the LLM:
   
   ทำตัวเป็นเพื่อนสนิทของผู้ใช้ การสนทนานี้เป็นการคุยกันด้วยเสียง ฉะนั้นตอบไม่เกินสองประโยค ชวนผู้ใช้คุยด้วยตนเอง
   
   You can write your own prompt here, or simply press [ENTER] to move on with the default prompt without typing anything.: 
   ```

4. Then the app will ask for your confirmation to start a conversation.

   ```plaintext
   Using default prompt...
   Start voice conversation? (y/n): y
   ```

5. You can start talking, enjoy!

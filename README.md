<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://ai.google.dev/static/site-assets/images/share-ais-513315318.png" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/44154556-824b-4ae8-a281-ad2bb4df3f6b

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

Awesome! I'm glad to hear you're happy with it. 

You now have a fully functional Python dashboard running on Streamlit that beautifully replicates your original design. You can continue to access it at **http://localhost:8503**.

To stop the server later on, you can simply close the terminal it's running in, or if you ever need to restart it in the future, just run `streamlit run app.py` from your project directory.

If you ever decide you want to upgrade the backend to use the full Machine Learning model, or if you need help with anything else, just let me know. Have a great time exploring your new dashboard!
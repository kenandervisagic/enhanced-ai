# 🧠 AI Content Generator for TikTok & YouTube Shorts

This is a simple AI-powered project designed to automatically generate engaging content for short-form platforms like **TikTok**, **YouTube Shorts**, and **Instagram Reels**.

The system uses AI to produce bite-sized scripts and text-based content ideal for visual storytelling, voiceovers, or automated video creation.

## ✨ What It Can Generate

1. **How to Survive** – survival tips or guides for extreme or everyday situations  
2. **Top 3** – quick lists with entertaining or informative rankings  
3. **Quotes** – AI-curated inspirational, thought-provoking, or emotional quotes  
4. **Lifehacks** – *(coming soon)* clever tricks to make life easier  

## 🚀 Purpose

The goal is to automate the creative process behind short-form video content — helping creators save time and maintain consistency while still producing engaging, valuable material.

## Examples:
[Top 3 Dirtiest Countries Exposed: India, Pakistan, Bangladesh | TikTok](https://www.tiktok.com/@ripples_of_the_web/video/7486178093724454190)


[Exploring the World's Most Dangerous Cults | TikTok](https://www.tiktok.com/@ripples_of_the_web/video/7489586758729125166)

---

## Setup Instructions

1. **Ensure Docker is running:**
   * Make sure Docker Desktop (or Docker Engine) is installed and running on your machine.


2. **Setup ```.env``` file:**
   ```bash
   cp .env-example .env
   ```
   * Replace ```OPENAI_API_KEY``` with your actual key
   * **Make sure to add the following based on your requirements:**
     * ```TOPIC_TYPE``` values can be <1, 2, 3, 4> which correspond 
       * 1 - How to survive
       * 2 - Top 3
       * 3 - Quotes
       * 4 - Lifehacks (to be implemented)
     * ```TOPIC``` value can be whatever topic the video should be about
       * **NOTE: ```TOPIC``` value does not have to be set if ```TOPIC_TYPE``` is 3 (quotes)**
     
   * Example .env file:
   ```bash
      OPENAI_API_KEY=supersecretkey
      TOPIC_TYPE=2
      TOPIC='Top 3 Most Dangerous Foods You Should Never Eat'
      ```

3. **Start the Docker containers:**
    ```bash
   docker compose up 
    ```

---
## PyCharm Setup

1. Set ```app``` as the Project Root:
   * Open PyCharm.
   * Right-click the ```app``` directory in the Project Explorer.
   * Select **Mark Directory as** → **Sources Root**. This will ensure that PyCharm can properly resolve imports and treat the app directory as the project root.

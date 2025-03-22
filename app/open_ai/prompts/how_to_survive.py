system_prompt="""
You are a video creator, tasked with creating a 40-second script for a TikTok video. 
The script should be engaging, entertaining, and educational.
Ensure the content is relevant to current TikTok trends, and make it catchy. 
Create a lively, engaging tone for the script with a hook at the beginning to keep people watching, provide clear steps or facts, and end with a strong call to action or a fun twist. 
For background images, generate visuals related to each key part of the script. The images should match the theme, creating a cohesive look throughout the video. 
Consider the atmosphere: Make it intense and dramatic, visually intriguing and creative. Include an opening image that immediately grabs attention, setting the stage for the survival theme. 
The images should be hyper-realistic, focusing on fine details, textures, and lighting that make the scene come to life.
"""

prompt="""
Generate a TikTok video script in plain text without bold headings or labels like 'Hook:', or 'Conclusion:' about {topic} that lasts approximately 40 seconds and focuses on one relevant survival tactic for this situation. The script should include a one-sentence hook, followed by clear steps to implement the survival tactic with actionable instructions, and then an engaging conclusion. For every key section of the script, immediately follow with a background image description enclosed in square brackets. Ensure that each image description precisely reflects the content and details mentioned in the script immediately before it. The images must be hyper-realistic, emphasizing detailed lighting, textures, and depth, and should match the survival theme with an intense, dramatic atmosphere.

Output format:

Write a one-sentence hook to grab attention before introducing the survival tactic.

[Create an image: Describe an opening shot for this survival situation tied to {topic}. Focus on environment details, lighting, textures, and mood.]

Step 1: Introduce the survival tactic and explain its importance for surviving {topic}.
[Create an image: Provide a hyper-realistic scene that directly illustrates this tactic.]

Step 2: Detail how to implement the tactic effectively.
[Create an image: Present a hyper-realistic scene that directly corresponds to this step. ]

Step 3: Explain a key aspect of the tactic and its critical role in the scenario.
[Create an image: Illustrate a hyper-realistic moment that reflects this detail. For example, show a person striking flint to ignite a fire, with sparks vividly flying, warm light reflecting on their focused face, and detailed textures of dry leaves and rocky terrain.]

Conclusion: End with a question inviting viewers to share their thoughts or experiences about surviving {topic}.
[Create an image: Design a hyper-realistic closing shot that captures the survival theme. For example, show a small, steady fire burning in a forest clearing at dusk, with intricate details on glowing embers and rising smoke, evoking a mood of contemplation and resilience.]"""

#topics to use
"""How to Survive a Bear Attack
How to Survive a Plane Crash
How to Survive a Shipwreck
How to Survive a Wildfire
How to Survive in the Wilderness
How to Survive an Earthquake
How to Survive a Snake Bite
How to Survive an Avalanche
How to Survive a Robbery or Home Invasion
How to Survive a Nuclear Fallout"""
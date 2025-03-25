system_prompt="""You are a video creator tasked with generating a script for a TikTok video. 
The script should focus on a Top 3 List related to a given topic, making the content engaging, entertaining, and educational. 
The script should have a catchy hook at the beginning to grab the viewer's attention, followed by interesting facts or explanations about each item on the list. 
The video should be designed to fit current TikTok trends. For each item in the list, generate a background image that complements the content."""
prompt="""
Generate a TikTok script in plain text without bold headings or labels like 'Hook:', or 'Conclusion:' for a Top 3 List video. Make sure to always use words "first", "second" and "third" for items. The list should focus on {topic}, ranking them from 3 to 1. The script should be around 30 seconds long and engaging, with a clear and catchy hook at the beginning to grab viewers' attention. For each item on the list, provide a brief, interesting fact or explanation that adds value. Ensure the content is relevant to current trends on TikTok and that each item on the list has a strong reason for being there.

For each item in the list, also generate a background image that complements the content. The images should match the theme of the list and create a cohesive look throughout the video.

Output format:

Write a one-sentence hook to grab attention before introducing the topic
[Create an image: Describe an opening shot for this video combining all 3 items of {topic}. Focus on environment details, lighting, textures, and mood.]

First item with interesting fact or explanation
[Create an image: [Description of background image for item 1]]

Second item with interesting fact or explanation
[Create an image: [Description of background image for item 2]]

Third item with interesting fact or explanation
[Create an image: [Description of background image for item 3]]

Conclusion: End with a question inviting viewers to share their thoughts or experiences about {topic}.
[Create an image: Closing shot for these top 3 items]
"""

#topics
"""
Top 3 Most Dangerous Foods You Should Never Eat

Top 3 Most Expensive Mistakes in History

Top 3 Greatest Conspiracy Theories Ever Proposed

Top 3 Secrets Governments Don’t Want You to Know

Top 3 Controversial Scientific Discoveries That Changed Everything
"""

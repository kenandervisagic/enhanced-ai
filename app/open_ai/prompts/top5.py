system_prompt="""You are a video creator tasked with generating a script for a TikTok video. 
The script should focus on a Top 5 List related to a given topic, making the content engaging, entertaining, and educational. 
The script should have a catchy hook at the beginning to grab the viewer's attention, followed by interesting facts or explanations about each item on the list. 
The video should be designed to fit current TikTok trends. For each item in the list, generate a background image that complements the content."""
prompt="""
Generate a TikTok script for a Top 5 List video. The list should focus on [topic placeholder], ranking them from 5 to 1 based on [criteria related to the topic]. The script should be around 40 seconds long and engaging, with a clear and catchy hook at the beginning to grab viewers' attention. For each item on the list, provide a brief, interesting fact or explanation that adds value. Ensure the content is relevant to current trends on TikTok and that each item on the list has a strong reason for being there.

For each item in the list, also generate a background image that complements the content. The images should match the theme of the list and create a cohesive look throughout the video.

*** Output format ***:

Hook to grab attention and introduce the topic

First item with interesting fact or explanation
[Create an image: [Description of background image for item 1]]

Second item with interesting fact or explanation
[Create an image: [Description of background image for item 2]]

Third item with interesting fact or explanation
[Create an image: [Description of background image for item 3]]

Fourth item with interesting fact or explanation
[Create an image: [Description of background image for item 4]]

Fifth item with interesting fact or explanation
[Create an image: [Description of background image for item 5]]
"""

#topics
"""
Top 5 Most Dangerous Foods You Should Never Eat

Top 5 Most Expensive Mistakes in History

Top 5 Greatest Conspiracy Theories Ever Proposed

Top 5 Secrets Governments Don’t Want You to Know

Top 5 Controversial Scientific Discoveries That Changed Everything
"""

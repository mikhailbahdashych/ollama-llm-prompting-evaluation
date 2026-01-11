"""Creative Writing task definition."""

from ..base import Task, TaskExample


def create_creative_writing_task() -> Task:
    """Create the Creative Writing evaluation task.

    This task evaluates the model's ability to generate creative,
    engaging, and well-structured narrative content.
    """
    return Task(
        id="creative_writing",
        name="Creative Writing",
        category="Generation",
        description="This task evaluates the model's ability to create original, engaging narrative content with coherent plot structure, vivid descriptions, and effective use of literary techniques.",
        evaluation_input="""Write a short story (approximately 200-300 words) that begins with the sentence: "The clock struck midnight, but time had stopped moving three hours ago."

Your story should:
- Have a clear beginning, middle, and end
- Include at least one interesting character
- Create a sense of atmosphere or mood
- Have an unexpected or thought-provoking element

Write the complete short story.""",
        expected_output_characteristics="An original short story that starts with the given sentence, demonstrates creative thinking about the concept of time stopping, includes vivid descriptions and character development, maintains narrative coherence, builds atmosphere effectively, and delivers a satisfying conclusion. The story should be engaging and show good command of narrative techniques.",
        development_examples=[
            TaskExample(
                input="""Write a brief scene (100-150 words) about a musician discovering an old instrument in an attic. Include sensory details.""",
                output="""The attic smelled of dust and forgotten memories as Sarah climbed the creaking wooden stairs. Sunlight streamed through a grimy window, illuminating motes dancing in the air. In the corner, beneath a moth-eaten blanket, something gleamed.

She uncovered it slowly—a violin, its wood the color of aged honey. The strings were slack, but the craftsmanship was extraordinary. Sarah's fingers trembled as she picked it up. The wood was cool and smooth, marked with tiny scratches that spoke of decades of use.

When she drew the bow across the strings, even out of tune, the sound that emerged was hauntingly beautiful. It was as if the instrument had been waiting, patient through the years, for someone to awaken its voice again.""",
                explanation="This example demonstrates vivid sensory details (smell, sight, touch, sound), creates atmosphere, develops character through action and emotion, and has a complete narrative arc with a satisfying resolution."
            ),
            TaskExample(
                input="""Write a two-paragraph story about someone finding an unexpected message. Make it intriguing.""",
                output="""The message was written in the steam on her bathroom mirror: "Remember what you forgot." Emma stared at the words, her heart pounding. She lived alone, and the apartment had been empty all day. The condensation from her shower couldn't have done this—she hadn't showered yet.

As she reached out to touch the mirror, her finger met not glass but paper. The mirror was a photograph, one she'd taken three years ago of this exact bathroom. And in the reflection behind her photographic self, barely visible in the steam, was a figure she'd never noticed before. Someone who had always been there, waiting to be seen.""",
                explanation="This creates mystery and suspense, uses an unexpected twist, builds tension effectively, and leaves the reader intrigued. It demonstrates strong narrative control in a very short space."
            )
        ],
        evaluation_criteria={
            "creativity": "Original and imaginative content",
            "coherence": "Story flows logically and maintains consistency",
            "engagement": "Writing is compelling and well-paced",
            "language_quality": "Good use of language and style"
        },
        scoring_rubric={
            "creativity": 5,
            "coherence": 5,
            "engagement": 5,
            "language_quality": 5
        },
        is_complete=True
    )

"""Language Understanding & Ambiguity task definition."""

from ..base import Task, TaskExample


def create_language_understanding_task() -> Task:
    """Create the Language Understanding & Ambiguity evaluation task.

    This task evaluates the model's ability to handle ambiguous language,
    understand nuances, and resolve linguistic ambiguity.
    """
    return Task(
        id="language_understanding",
        name="Language Understanding & Ambiguity",
        category="Understanding",
        description="This task evaluates the model's ability to recognize and resolve linguistic ambiguity, understand context-dependent meanings, interpret idioms and figurative language, and grasp subtle nuances in communication.",
        evaluation_input="""Analyze the following sentences for ambiguity and nuance. For each, explain the ambiguity or nuance, provide the different possible interpretations, and explain which interpretation is more likely given context clues.

1. "I saw the man with the telescope."
   - What is ambiguous about this sentence?
   - What are the different possible meanings?

2. "The chicken is ready to eat."
   - Explain the ambiguity in this sentence.
   - What are the two different scenarios this could describe?

3. "After months of practice, the pianist finally made her parents proud."
   - What does this sentence imply about the situation before "months of practice"?
   - What nuance or subtext might be present in this statement?

Provide thorough analysis of each sentence.""",
        expected_output_characteristics="A response that correctly identifies syntactic and semantic ambiguities, explains how the same sentence structure can yield different meanings, demonstrates understanding of pragmatic implicature (what's implied but not explicitly stated), and shows awareness of how context shapes interpretation. The answer should distinguish between literal and implied meanings.",
        development_examples=[
            TaskExample(
                input="""Analyze this sentence for ambiguity: "Visiting relatives can be boring."

What makes this sentence ambiguous? Explain the different interpretations.""",
                output="""This sentence contains a syntactic ambiguity based on how "visiting" is interpreted:

Interpretation 1: "Visiting relatives" as a noun phrase (relatives who are visiting)
- Meaning: When your relatives come to visit you, it can be boring
- "Visiting" functions as an adjective modifying "relatives"

Interpretation 2: "Visiting relatives" as a verb phrase (the act of visiting relatives)
- Meaning: When you go to visit your relatives, it can be boring
- "Visiting" functions as a gerund (verb acting as a noun)

Both interpretations are grammatically valid with the exact same word sequence. Without additional context, we can't determine which meaning is intended. This is a classic example of structural ambiguity where the grammatical role of words can change the entire meaning of the sentence.""",
                explanation="This correctly identifies the syntactic ambiguity, explains both interpretations clearly, and notes that the sentence structure itself creates the ambiguity without additional context."
            ),
            TaskExample(
                input="""What does this phrase mean: "She's cool as a cucumber during presentations."

Explain both the literal impossibility and the actual meaning.""",
                output="""This is an idiom that uses figurative language:

Literal interpretation (not the intended meaning):
- It would mean her body temperature is as cold as a cucumber, which is impossible and makes no sense

Actual idiomatic meaning:
- She remains calm, composed, and unruffled during presentations
- She doesn't show nervousness or anxiety even in stressful situations
- She maintains her poise and confidence

The idiom "cool as a cucumber" uses "cool" metaphorically to mean calm and collected rather than referring to temperature. This phrase relies on shared cultural/linguistic knowledge - someone unfamiliar with English idioms might interpret it literally and be confused. The comparison to a cucumber specifically (rather than other cold objects) is arbitrary and conventional to this particular idiom.""",
                explanation="This demonstrates understanding of figurative vs. literal language, explains the idiomatic meaning, and shows awareness that idioms require cultural/linguistic knowledge beyond literal word meanings."
            )
        ],
        evaluation_criteria={
            "disambiguation": "Correctly identifies and resolves ambiguity",
            "nuance_recognition": "Recognizes subtle meanings and implications",
            "explanation_clarity": "Clearly explains the interpretation"
        },
        scoring_rubric={
            "disambiguation": 10,
            "nuance_recognition": 5,
            "explanation_clarity": 5
        },
        is_complete=True
    )

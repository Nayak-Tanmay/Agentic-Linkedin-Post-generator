def decision_agent(evaluation):

    if hasattr(evaluation, "model_dump"):
        evaluation = evaluation.model_dump()

    if evaluation["overall_score"] >= 8.5:
        return "end"

    elif evaluation["research_quality_score"] < 7:
        return "research"

    else:
        return "revise"
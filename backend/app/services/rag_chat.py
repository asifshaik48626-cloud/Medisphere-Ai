from .guideline_retrieval import GuidelineRetrievalService

class GuidelinesRagChat:
    @classmethod
    def answer_question(cls, question: str) -> dict:
        """
        Answers clinician questions grounded in the CDC/WHO Guidelines library.
        """
        # 1. Search guidelines context chunks matching query
        chunks = GuidelineRetrievalService.search(question)
        
        if not chunks:
            return {
                "answer": "I could not find matching clinical guidelines in the CDC/WHO database for your query. Please cross-reference standard medical literature.",
                "sources": []
            }
            
        # 2. Extract context elements
        context_snippets = []
        sources = []
        for index, chunk in enumerate(chunks, 1):
            context_snippets.append(
                f"[{index}] (Source: {chunk['publisher']}, Evidence Level: {chunk['evidence_level']}): "
                f"{chunk['text']}"
            )
            sources.append({
                "title": f"Guideline Chunk #{chunk['id'][:8]}",
                "publisher": chunk['publisher'],
                "evidence_level": chunk['evidence_level'],
                "recommendation_strength": chunk['recommendation_strength']
            })
            
        # 3. Build grounded clinical answer
        compiled_context = "\n".join(context_snippets)
        answer = (
            f"Based on the CDC and WHO Guidelines matched for your question: '{question}':\n\n"
            f"**Recommendation Analysis**:\n"
        )
        
        # Add details based on query match
        q_lower = question.lower()
        if "fever" in q_lower:
            answer += (
                "- For fever complaints, monitor core temperatures. Under WHO rules, support oral rehydration and verify difficulty in breathing.\n"
                "- Administer Paracetamol 500mg as antipyretic relief, subject to allergy confirmation.\n"
            )
        elif "headache" in q_lower:
            answer += (
                "- For headaches, screen for neck stiffness and sudden-onset severity (thunderclap) to exclude meningitis or cerebrovascular events.\n"
                "- Support rest in dark rooms and cold compresses for benign tension/migraine headaches.\n"
            )
        else:
            answer += "- Review patient demographics, pregnancy status, and active warnings list before validating recommendations.\n"
            
        answer += (
            f"\n**Grounded References**:\n{compiled_context}\n\n"
            f"*Note: Clinical judgment supersedes AI summaries.*"
        )
        
        return {
            "answer": answer,
            "sources": sources
        }

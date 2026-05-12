from __future__ import annotations


class PreviewService:
    """HTML slide preview renderer for Streamlit."""

    def render_slide_container(self) -> str:
        return """
        <div style="
            width: 100%;
            aspect-ratio: 16 / 9;
            background: white;
            border-radius: 24px;
            border: 1px solid #E5E7EB;
            padding: 24px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.06);
            margin-bottom: 24px;
        ">
        </div>
        """

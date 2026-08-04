import os
from analyzer import analyze_skin_image
import gradio as gr

def medscan(image):
    if image is None:
        return "Please upload an image."
    verdict, risk, warnings, sym, edges, color = analyze_skin_image(image)
    warning_text = "\n".join(f"• {w}" for w in warnings) if warnings else "• No warning signs"
    stats = f"Symmetry: {sym:.1f}% | Edges: {edges:.1f}% | Color var: {color:.1f}"
    return f"{verdict}\n\nRisk: {risk}/75\n\n{warning_text}\n\n{stats}"

demo = gr.Interface(
    fn=medscan,
    inputs=gr.Image(type="pil", label="Upload skin image"),
    outputs=gr.Textbox(label="Results"),
    title="MedScan v0.1",
    description="A.I. Biotech, Prototype. NOT a medical device."
)

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))

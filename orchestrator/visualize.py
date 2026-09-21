from graph import app

def generate_graph_image():
    print("Generating graph image...")
    
    # get_graph() builds the structure without executing the nodes
    png_data = app.get_graph().draw_mermaid_png()
    
    # Save the binary data to a PNG file
    with open("architecture_graph.png", "wb") as f:
        f.write(png_data)
        
    print(" -> Successfully saved: architecture_graph.png")

if __name__ == "__main__":
    generate_graph_image()
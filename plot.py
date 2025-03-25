import streamlit as st
import subprocess
import os

# Default Vina path
DEFAULT_VINA_PATH = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"


# Function to run docking
def run_vina(vina_path, receptor, ligand, center_x, center_y, center_z, size_x, size_y, size_z):
    if not os.path.exists(vina_path):
        return "Error: AutoDock Vina executable not found. Check the path!"

    command = [
        vina_path,
        "--receptor", receptor,
        "--ligand", ligand,
        "--center_x", str(center_x),
        "--center_y", str(center_y),
        "--center_z", str(center_z),
        "--size_x", str(size_x),
        "--size_y", str(size_y),
        "--size_z", str(size_z),
        "--out", "docked_output.pdbqt",
    ]

    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        return process.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: Docking failed.\n\nVina Error Log:\n{e.stderr}"


# Streamlit UI
st.title("Molecular Docking with AutoDock Vina")

# Vina path selection
st.subheader("AutoDock Vina Configuration")
use_default = st.checkbox("Use default Vina path", value=True)

vina_path = DEFAULT_VINA_PATH
if not use_default:
    custom_path = st.text_input("Enter custom path to Vina executable", value="")
    if custom_path:
        vina_path = custom_path

# Upload receptor and ligand
st.subheader("Upload Files")
receptor_file = st.file_uploader("Upload Receptor (PDBQT)", type=["pdbqt"])
ligand_file = st.file_uploader("Upload Ligand (PDBQT)", type=["pdbqt"])

# Define docking parameters
st.subheader("Define Docking Box")
col1, col2 = st.columns(2)
with col1:
    center_x = st.number_input("Center X", value=0.0)
    center_y = st.number_input("Center Y", value=0.0)
    center_z = st.number_input("Center Z", value=0.0)
with col2:
    size_x = st.number_input("Size X (Å)", value=20.0)
    size_y = st.number_input("Size Y (Å)", value=20.0)
    size_z = st.number_input("Size Z (Å)", value=20.0)

if st.button("Run Docking"):
    if receptor_file and ligand_file:
        # Save uploaded files
        receptor_path = "receptor.pdbqt"
        ligand_path = "ligand.pdbqt"

        with open(receptor_path, "wb") as f:
            f.write(receptor_file.getbuffer())
        with open(ligand_path, "wb") as f:
            f.write(ligand_file.getbuffer())

        # Run docking
        result = run_vina(vina_path, receptor_path, ligand_path,
                          center_x, center_y, center_z,
                          size_x, size_y, size_z)

        # Display results
        st.subheader("Results")
        st.text_area("Vina Output", result, height=300)

        # Add download button for output file
        if os.path.exists("docked_output.pdbqt"):
            with open("docked_output.pdbqt", "rb") as f:
                st.download_button("Download Docked Results", f, file_name="docked_output.pdbqt")
    else:
        st.error("Please upload both receptor and ligand files.")
import os
from pathlib import Path

path_dir_data_base = "/Users/tchi/Dev_TohokuUniv/icdLab/document-video-snapshot-analysis-test/src/backend_testing/.data"
path_dir_data_pdf_analyzed = os.path.join(
    path_dir_data_base, "document_pdf_analyzed"
)
path_dir_data_activities_analyzed = os.path.join(
    path_dir_data_base, "document_activities_analyzed"
)

path_file_document_concat_img = lambda asset_id: os.path.join(
    path_dir_data_pdf_analyzed, f"{asset_id}.concat.png"
)

path_file_document_index = lambda asset_id: os.path.join(
    path_dir_data_pdf_analyzed, f"{asset_id}.index.json"
)

path_file_video = lambda asset_id: os.path.join(
    path_dir_data_base, f"{asset_id}.mp4"
)

path_file_scroll_tl = lambda asset_id: os.path.join(
    path_dir_data_activities_analyzed,
    f"{asset_id}.scroll.json",
)

path_file_tessearct_bin = "/opt/homebrew/bin/tesseract"
# path_file_tessearct_bin = "C:/Users/tchi0/AppData/Local/Tesseract-OCR/tesseract.exe"


path_dir_output_front = os.path.join(
    Path(__file__).parent.parent.parent,
    "visualization-app",
    "src",
    "data",
)


path_dir_output_back = os.path.join(
    Path(__file__).parent.parent,
    "data",
)

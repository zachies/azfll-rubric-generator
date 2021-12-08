class DataContext:
    def __init__(self, pdf_template_path: str = None, data_sheet_paths: list = list(), recipe_path: str = None, output_dir_path: str = None) -> None:
        self.pdf_template_path = pdf_template_path
        self.data_sheet_paths = data_sheet_paths
        self.recipe_path = recipe_path
        self.output_dir_path = output_dir_path
import tkinter, tkinter.filedialog
from tkinter.constants import E, N, S, W
from tkinter.ttk import *
from controllers.generator import Generator

from models.DataContext import DataContext

class MainView():
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.window.title("AZFLL Rubrics Generator")
        # self.window.geometry("600x400")

        self.__init_widgets__()
        self.data_context = DataContext()

        self.window.mainloop()

    def __init_widgets__(self) -> None:
        window = self.window

        # Step text (column 0)
        tkinter.ttk.Label(window, text = "1)").grid(row=1, column=0, padx=10, pady=10)
        tkinter.ttk.Label(window, text = "2)").grid(row=2, column=0, padx=10, pady=10)
        tkinter.ttk.Label(window, text = "3)").grid(row=3, column=0, padx=10, pady=10)
        tkinter.ttk.Label(window, text = "4)").grid(row=4, column=0, padx=10, pady=10)
        # tkinter.ttk.Label(window, text = "5)").grid(row=5, column=0, padx=10, pady=10)

        # Buttons (column 1)
        self.select_pdf_button    = tkinter.ttk.Button(self.window, text="Select Template PDF",       padding=5, command=self.select_pdf_button_triggered)
        self.select_data_button   = tkinter.ttk.Button(self.window, text="Select Data from Source",   padding=5, command=self.select_data_button_triggered)
        # self.select_recipe_button = tkinter.ttk.Button(self.window, text="Select Recipe from Source", padding=5, command=self.select_recipe_button_triggered)
        self.select_output_button = tkinter.ttk.Button(self.window, text="Select Output Directory",   padding=5, command=self.select_output_button_triggered)
        self.generate_button      = tkinter.ttk.Button(self.window, text="Generate PDFs",             padding=5, command=self.generate_button_triggered)

        self.select_pdf_button.grid(row=1, column=1, padx=10, pady=10, sticky=N+S+E+W)
        self.select_data_button.grid(row=2, column=1, padx=10, pady=10, sticky=N+S+E+W)
        # self.select_recipe_button.grid(row=3, column=1, padx=10, pady=10, sticky=N+S+E+W)
        self.select_output_button.grid(row=3, column=1, padx=10, pady=10, sticky=N+S+E+W)
        self.generate_button.grid(row=4, column=1, padx=10, pady=10, sticky=N+S+E+W)

        # Status text (column 2)
        self.select_pdf_status    = tkinter.ttk.Label(self.window, text="Waiting for input...", padding=5)
        self.select_data_status   = tkinter.ttk.Label(self.window, text="Missing requirements. No PDF template selected.", padding=5)
        # self.select_recipe_status = tkinter.ttk.Label(self.window, text="Missing requirements. No data selected.", padding=5)
        self.select_output_status = tkinter.ttk.Label(self.window, text="Missing requirements. No recipe selected.", padding=5)
        self.generate_status      = tkinter.ttk.Label(self.window, text="Missing requirements.", padding=5)

        self.select_pdf_status.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        self.select_data_status.grid(row=2, column=2, padx=10, pady=10, sticky=W)
        # self.select_recipe_status.grid(row=3, column=2, padx=10, pady=10, sticky=W)
        self.select_output_status.grid(row=3, column=2, padx=10, pady=10, sticky=W)
        self.generate_status.grid(row=4, column=2, padx=10, pady=10, sticky=W)

        # Default states for program
        self.__select_pdf_button_ready__()
        self.__select_data_button_disabled__()
        # self.__select_recipe_button_disabled__()
        self.__select_output_button_disabled__()
        self.__generate_button_disabled__()



    ### Select PDF Button
    def __select_pdf_button_ready__(self) -> None:
        self.select_pdf_status.configure(text="Waiting for input...", foreground="black")

    def __select_pdf_button_validated__(self, status_text: str) -> None:
        self.select_pdf_status.configure(text="PDF selected: {}".format(status_text), foreground="green")

    ### Select Data Button
    def __select_data_button_ready__(self) -> None:
        self.select_data_status.configure(text="Waiting for input...", foreground="black")
        self.set_button_state(self.select_data_button, True)

    def __select_data_button_validated__(self, status_text: str) -> None:
        self.select_data_status.configure(text="Sheets selected: {}".format(status_text), foreground="green")

    def __select_data_button_disabled__(self) -> None:
        self.select_data_status.configure(text="Missing requirements. No PDF template selected.", foreground="gray")
        self.set_button_state(self.select_data_button, False)

    # ### Select Recipe Button
    # def __select_recipe_button_ready__(self) -> None:
    #     self.select_recipe_status.configure(text="Waiting for input...", foreground="black")
    #     self.set_button_state(self.select_recipe_button, True)

    # def __select_recipe_button_validated__(self, status_text: str) -> None:
    #     self.select_recipe_status.configure(text="Recipe selected: {}".format(status_text), foreground="green")

    # def __select_recipe_button_disabled__(self) -> None:
    #     self.select_recipe_status.configure(text="Missing requirements. No data selected.", foreground="gray")
    #     self.set_button_state(self.select_recipe_button, False)

    ### Select Output Button
    def __select_output_button_ready__(self) -> None:
        self.select_output_status.configure(text="Waiting for input...", foreground="black")
        self.set_button_state(self.select_output_button, True)

    def __select_output_button_validated__(self, status_text: str) -> None:
        self.select_output_status.configure(text="Output directory: {}".format(status_text), foreground="green")

    def __select_output_button_disabled__(self) -> None:
        self.select_output_status.configure(text="Missing requirements. No recipe selected.", foreground="gray")
        self.set_button_state(self.select_output_button, False)

    ### Generate Button
    def __generate_button_ready__(self) -> None:
        self.generate_status.configure(text="Ready to generate...", foreground="black")
        self.set_button_state(self.generate_button, True)

    def __generate_button_validated(self, status_text: str) -> None:
        self.generate_status.configure(text="Files generated: {}".format(status_text), foreground="green")

    def __generate_button_disabled__(self) -> None:
        self.generate_status.configure(text="Missing requirements.", foreground="gray")
        self.set_button_state(self.generate_button, False)

    def __generate_button_error__(self, status_text: str) -> None:
        self.generate_status.configure(text=status_text, foreground="red")
        self.set_button_state(self.generate_button, True)

    ### Events
    def select_pdf_button_triggered(self) -> None:
        print("[EVENT] select_pdf_button was pressed.")
        selection = tkinter.filedialog.askopenfilename(title="Select template PDF file", filetypes=[("PDF File", "*.pdf")])
        if(selection):
            print("[EVENT] user entered a file in select_pdf_button_triggered: {}".format(selection))
            filename = ((selection[::-1]).split('/')[0])[::-1]
            self.data_context.pdf_template_path = selection
            self.__select_data_button_ready__()
            self.__select_pdf_button_validated__(filename)
        else:
            self.__generate_button_disabled__()
            self.__select_pdf_button_ready__()

    def select_data_button_triggered(self) -> None:
        print("[EVENT] select_data_button was pressed.")
        selections = tkinter.filedialog.askopenfilenames(title="Select data files", filetypes=[("Tab-Separated Values File", "*.tsv")])
        if(selections):
            print("[EVENT] user entered files in select_data_button_triggered: {}".format(selections))
            self.data_context.data_sheet_paths = selections
            self.__select_data_button_validated__(len(selections))
            # self.__select_recipe_button_ready__()
            self.__select_output_button_ready__()
        else:
            self.__select_data_button_ready__()
            self.__generate_button_disabled__()

    # def select_recipe_button_triggered(self) -> None:
    #     print("[EVENT] select_recipe_button was pressed.")
    #     selection = tkinter.filedialog.askopenfilename(title="Select recipe file", filetypes=[("Recipe File", "*.recipe")])
    #     if(selection):
    #         print("[EVENT] user entered a file in select_recipe_button_triggered: {}".format(selection))
    #         filename = ((selection[::-1]).split('/')[0])[::-1]
    #         self.data_context.pdf_template_path = selection
    #         self.__select_output_button_ready__()
    #         # self.__select_recipe_button_validated__(filename)
    #         lexer = LexicalAnalyzer(filename)
    #         for tok in lexer.lexer:
    #             print(tok)
    #     else:
    #         self.__generate_button_disabled__()
    #         # self.__select_recipe_button_ready__()

    def select_output_button_triggered(self) -> None:
        print("[EVENT] select_output_button was pressed.")
        selection = tkinter.filedialog.askdirectory(title="Select output directory", mustexist=True)
        if(selection):
            print("[EVENT] user entered a file in select_output_button_triggered: {}".format(selection))
            self.data_context.output_dir_path = selection
            self.__generate_button_ready__()
            if(len(selection) > 40):
                temp = "..." + selection[-40:]
            else:
                temp = selection
            self.__select_output_button_validated__(temp)
        else:
            self.__select_output_button_ready__()
            self.__generate_button_disabled__()

    def generate_button_triggered(self) -> None:
        print("[EVENT] generate_button was pressed.")
        try:
            msg = Generator(self.data_context).result
            self.__generate_button_validated(msg)
        except Exception as e:
            self.__generate_button_error__(str(e))



    ### Methods
    def set_button_state(self, button: tkinter.ttk.Button, state: bool) -> None:
        if state == True:
            button.state(["!disabled"])
        else:
            button.state(["disabled"])
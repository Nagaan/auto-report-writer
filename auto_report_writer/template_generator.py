import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

class XMLVulnerabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vulnerability Report")

        # Initialize XML tree
        self.tree = None

        # File upload button
        self.upload_btn = tk.Button(root, text="Upload XML File", command=self.upload_file)
        self.upload_btn.pack(pady=10)

        # Dropdowns
        self.create_dropdown("Root Element:", "root_element", self.update_subroot_dropdown)
        self.create_dropdown("Subroot Element (optional):", "subroot_element", self.update_vulnerability_name_dropdown)
        self.create_dropdown("Vulnerability Name:", "vulnerability_name", self.update_detail_dropdowns)
        self.create_dropdown("Risk Level (optional):", "risk_level", self.no_action)
        self.create_dropdown("CVSS Score (optional):", "cvss_score", self.no_action)

        # Vulnerability Details
        self.details_label = tk.Label(root, text="Vulnerability Details:")
        self.details_label.pack()
        self.detail_vars = [tk.StringVar(root) for _ in range(3)]
        self.detail_menus = [self.create_detail_dropdown(f"Element {i+1}:", i) for i in range(3)]

        # Submit button
        self.submit_btn = tk.Button(root, text="Submit", command=self.submit)
        self.submit_btn.pack(pady=20)

    def create_dropdown(self, label_text, attr_name, update_func):
        label = tk.Label(self.root, text=label_text)
        label.pack()
        var = tk.StringVar(self.root)
        setattr(self, attr_name + "_var", var)
        menu = tk.OptionMenu(self.root, var, "", command=lambda _: update_func())
        menu.pack(pady=5)
        setattr(self, attr_name + "_menu", menu)

    def create_detail_dropdown(self, label_text, index):
        label = tk.Label(self.root, text=label_text)
        label.pack()
        var = self.detail_vars[index]
        menu = tk.OptionMenu(self.root, var, "", command=lambda _: self.show_next_detail(index + 1))
        menu.pack(pady=5)
        if index > 0:
            label.pack_forget()
            menu.pack_forget()
        return menu

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.parse_xml(file_path)
            self.populate_root_dropdown()

    def parse_xml(self, file_path):
        self.tree = ET.parse(file_path)
        self.root_element = self.tree.getroot()

    def populate_root_dropdown(self):
        if not self.tree:
            return
        root_element_choices = self.get_all_descendants(self.root_element)
        self.update_dropdown_menu(self.root_element_menu, root_element_choices, self.root_element_var)

    def update_dropdown_menu(self, menu, choices, var):
        menu["menu"].delete(0, "end")
        for choice in choices:
            menu["menu"].add_command(label=choice, command=tk._setit(var, choice))
        var.set('Select an element')

    def get_all_descendants(self, element):
        descendants = set()
        for child in element.iter():
            if child is not element:
                descendants.add(child.tag)
        return descendants

    def update_subroot_dropdown(self):
        root_element_tag = self.root_element_var.get()
        if root_element_tag == 'Select an element':
            return
        root_element = self.root_element.find(".//" + root_element_tag)
        if root_element is not None:
            subroot_choices = self.get_all_descendants(root_element)
            self.update_dropdown_menu(self.subroot_element_menu, subroot_choices, self.subroot_element_var)

    def update_vulnerability_name_dropdown(self):
        root_element_tag = self.root_element_var.get()
        subroot_element_tag = self.subroot_element_var.get()
        if root_element_tag == 'Select an element':
            return
        root_element = self.root_element.find(".//" + root_element_tag)
        if subroot_element_tag == 'Select an element' and root_element is not None:
            vuln_choices = self.get_all_descendants(root_element)
            self.update_dropdown_menu(self.vulnerability_name_menu, vuln_choices, self.vulnerability_name_var)
        elif root_element is not None:
            subroot_element = root_element.find(".//" + subroot_element_tag)
            if subroot_element is not None:
                vuln_choices = self.get_all_descendants(subroot_element)
                self.update_dropdown_menu(self.vulnerability_name_menu, vuln_choices, self.vulnerability_name_var)

    def update_detail_dropdowns(self):
        root_element_tag = self.root_element_var.get()
        subroot_element_tag = self.subroot_element_var.get()
        vulnerability_name_tag = self.vulnerability_name_var.get()
        if root_element_tag == 'Select an element':
            return
        root_element = self.root_element.find(".//" + root_element_tag)
        if root_element is not None:
            if subroot_element_tag == 'Select an element':
                vuln_element = root_element.find(".//" + vulnerability_name_tag)
            else:
                subroot_element = root_element.find(".//" + subroot_element_tag)
                if subroot_element is not None:
                    vuln_element = subroot_element.find(".//" + vulnerability_name_tag)
            if vuln_element is not None:
                detail_choices = self.get_all_descendants(vuln_element)
                for var, menu in zip(self.detail_vars, self.detail_menus):
                    self.update_dropdown_menu(menu, detail_choices, var)

    def show_next_detail(self, index):
        if index < 3:
            label = self.root.pack_slaves()[index + 6]
            menu = self.detail_menus[index]
            label.pack()
            menu.pack()

    def submit(self):
        root_element = self.root_element_var.get()
        subroot_element = self.subroot_element_var.get()
        vulnerability_name = self.vulnerability_name_var.get()
        risk_level = self.risk_level_var.get()
        cvss_score = self.cvss_score_var.get()

        if root_element == 'Select an element' or vulnerability_name == 'Select an element':
            messagebox.showerror("Error", "Root Element and Vulnerability Name are required.")
            return

        details = {var.get(): "" for var in self.detail_vars if var.get() != 'Select an element'}
        if not details:
            messagebox.showerror("Error", "At least one element must be selected for Vulnerability Details.")
            return

        summary = (
                f"Root Element: {root_element}\n"
                f"Subroot Element: {subroot_element}\n"
                f"Vulnerability Name: {vulnerability_name}\n"
                f"Risk Level: {risk_level}\n"
                f"CVSS Score: {cvss_score}\n"
                "Details:\n" +
                "\n".join([f"{key}: {value}" for key, value in details.items()])
        )

        root_elem = ET.Element(root_element)
        if subroot_element != 'Select an element':
            subroot_elem = ET.SubElement(root_elem, subroot_element)
            vuln_elem = ET.SubElement(subroot_elem, vulnerability_name)
        else:
            vuln_elem = ET.SubElement(root_elem, vulnerability_name)

        if risk_level != 'Select an element':
            ET.SubElement(vuln_elem, "risk_level").text = risk_level
        if cvss_score != 'Select an element':
            ET.SubElement(vuln_elem, "cvss_score").text = cvss_score

        for key, value in details.items():
            ET.SubElement(vuln_elem, key).text = value

        tree = ET.ElementTree(root_elem)
        file_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if file_path:
            tree.write(file_path)

        messagebox.showinfo("Summary", summary)

    def no_action(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = XMLVulnerabilityApp(root)
    root.mainloop()

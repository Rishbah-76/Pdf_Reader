import pikepdf
import re
from pathlib import Path
import os
from pdfReader.utils.common import read_yaml,create_directories
from pdfReader import logger

config_filepath = Path("config.yaml")
config = read_yaml(config_filepath)
upload_folder=config.upload_folder.UPLOAD_FOLDER

class Rotatepdf:
    def __init__(self):
        config_filepath = Path("config.yaml")
        self.config = read_yaml(config_filepath)
        create_directories([self.config.pdf_output.filepath])
        print(os.listdir())
        self.output_filepath= self.config.pdf_output.filepath
        self.upload_folder=self.config.upload_folder.UPLOAD_FOLDER


    def all(self,deg_of_rotation: int,filepath: Path):
        #to rotate all the pages
        with pikepdf.Pdf.open(filepath) as my_pdf:
            for page in my_pdf.pages:
                page.Rotate = deg_of_rotation*90
            angle_of_rotation=90*deg_of_rotation
            new_pdf=Path(os.path.join(self.output_filepath,f"test.pdf" ))
            #angle_of_rotation: {angle_of_rotation} page_number: {page_No}")
            logger.info("Saving the pdf to new file: {new_pdf}")
            my_pdf.save(new_pdf)
            logger.info("Rotation completed>>> Process Ended successfully")
        return (new_pdf, angle_of_rotation, 'All')

    #all(deg_of_rotation=1,filepath='../uploads/project_report_shivam_new.pdf')


    def specific_page(self,page_No: int,deg_of_rotation: int,filepath: Path):
        #to rotate a specific pages
        with pikepdf.Pdf.open(filepath) as my_pdf:
            my_pdf.pages[page_No-1].Rotate = deg_of_rotation*90
            angle_of_rotation=90*deg_of_rotation
            new_pdf=Path(os.path.join(self.output_filepath,f"test.pdf" ))
            #angle_of_rotation: {angle_of_rotation} page_number: {page_No}")
            logger.info("Saving the pdf to new file: {new_pdf}")
            my_pdf.save(new_pdf)
            logger.info("Rotation completed>>> Process Ended successfully")
            return (new_pdf, angle_of_rotation, page_No)
    #specific_page(page_No=2,deg_of_rotation=1,filepath='../uploads/project_report_shivam_new.pdf')


    def list_of_pages(self,page_No: str,deg_of_rotation: int,filepath: Path):
        #to rotate a specific pages
        with pikepdf.Pdf.open(filepath) as my_pdf:
            page_No.lower()
            page_No=page_No.strip()
            page_No_str = re.split(r'-',page_No )
            logger.info(page_No_str)
            ini_page=int(page_No_str[0])
            last_page=int(page_No_str[1])
            
            for i in range(ini_page,last_page+1):
                my_pdf.pages[i-1].Rotate = deg_of_rotation*90

            angle_of_rotation=90*deg_of_rotation
            new_pdf=Path(os.path.join(self.output_filepath,f"test.pdf" ))
            #angle_of_rotation: {angle_of_rotation} page_number: {page_No}")
            logger.info("Saving the pdf to new file: {new_pdf}")
            my_pdf.save(new_pdf)
            logger.info("Rotation completed>>> Process Ended successfully")
            return (new_pdf, angle_of_rotation, page_No)

    #list_of_pages(page_No='2-7',deg_of_rotation=1,filepath='../uploads/project_report_shivam_new.pdf')
            


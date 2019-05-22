import PyPDF2
import os
import glob


def extract_and_combine_first_pages(pdf_files, output_pdf_dir,
                                    output_pdf_filename="_combined_first_pages.pdf"):
    """Extract and combine first pages of a list of pdf files

    Some files does not conform to the strict pdf format, use strict=False and make
    the following changes to the library:
        https://github.com/mstamy2/PyPDF3/issues/7

    Args:
        pdf_files: list of pdf paths

    Returns:

    """
    print('Combining \n  {}'.format('\n  '.join(pdf_files)))

    pdfWriter = PyPDF2.PdfFileWriter()
    for files_address in pdf_files:
        pdfFileObj = open(files_address, 'rb')
        try:
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
        except:
            print('Bad file {}'.format(files_address))
        pageObj = pdfReader.getPage(0)
        pdfWriter.addPage(pageObj)

    # if os.path.isfile(output_pdf_path):
    #     raise IOError('File exist! Please remove {} first'.format(output_pdf_path))

    output_pdf_path = os.path.join(output_pdf_dir, output_pdf_filename)
    with open(output_pdf_path, "wb") as output:
        pdfWriter.write(output)


def batch_extract_from_folder(source_pdf_dir, output_pdf_dir,
                              output_pdf_filename="_combined_first_pages.pdf"):
    pdf_files = glob.glob(os.path.join(source_pdf_dir, '*.pdf'))
    pdf_files = [x for x in pdf_files if not os.path.basename(x).startswith('_')]
    pdf_files.sort(key=str.lower)  # extract and combine in order
    extract_and_combine_first_pages(pdf_files[:], output_pdf_dir=output_pdf_dir,
                                    output_pdf_filename=output_pdf_filename)


if __name__ == '__main__':
    target_folder = "/Users/pliu/github/cvpr2019_downloader/papers"
    batch_extract_from_folder(source_pdf_dir=target_folder, output_pdf_dir=target_folder)

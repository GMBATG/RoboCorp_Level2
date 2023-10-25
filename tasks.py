from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    # browser.configure(
    #     slowmo=1000,
    # )

    open_robot_order_website()
    orderTable = get_orders()

    page = browser.page()
    page.click("text=Ok")

    for orderRow in orderTable:
        fill_the_form(orderRow)  

    archive_receipts()     



def open_robot_order_website():
    ''' Navigates to web site '''
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def get_orders():
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

    tables = Tables()
    orderTable = tables.read_table_from_csv(path="orders.csv", header=True, delimiters=",")
    #orderTable = Tables.read_table_from_csv(tables, path="orders.csv", header=True, delimiters=",")

    return orderTable


def fill_the_form(orderRow):
    page = browser.page()

    # Select Combo HEAD
    page.select_option("#head", orderRow["Head"])

    #page.get_by_label("1. Head:").select_option(str(orderRow["Head"]))

    #Click BODY
    if orderRow["Body"] == "1":
         page.get_by_text("Roll-a-thor body").click()
    elif orderRow["Body"] == "2":
        page.get_by_text("Peanut crusher body").click()
    elif orderRow["Body"] == "3":
        page.get_by_text("D.A.V.E body").click()
    elif orderRow["Body"] == "4":
        page.get_by_text("Andy Roid body").click()
    elif orderRow["Body"] == "5":
        page.get_by_text("Spanner mate body").click()
    elif orderRow["Body"] == "6":
        page.get_by_text("Drillbit 2000 body").click()

    #Enter LEGS
    page.get_by_placeholder("Enter the part number for the legs").fill(str(orderRow["Legs"]))
    
    #Enter ADDRESS
    page.get_by_placeholder("Shipping address").fill(orderRow["Address"])

    page.click("text=Preview")
    
    #page.click("text=Order")
    page.locator("#order").click()
    error = page.locator('.alert.alert-danger').count() > 0  

    while error:
        page.locator("#order").click()   
        error = page.locator('.alert.alert-danger').count() > 0  

    store_receipt_as_pdf(str(orderRow["Order number"]))    
    
    page.locator("#order-another").click()
    #page.click("text=Order another robot")
    page.click("text=Ok")


def store_receipt_as_pdf(order_number):
    page = browser.page()
    order_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(order_html, f"output/receipts/{order_number}.pdf")

    page.screenshot(path="output/screenshot.png")  
    embed_screenshot_to_receipt("output/screenshot.png", f"output/receipts/{order_number}.pdf") 

 
def embed_screenshot_to_receipt(screenshot, pdf_file):
    pdf = PDF()
    pdf.add_files_to_pdf(files=[screenshot], target_document=pdf_file, append=True)


def archive_receipts():   
    lib = Archive()
    lib.archive_folder_with_zip("output/receipts", "output/archive.zip")



  
#order_robots_from_RobotSpareBin()

    

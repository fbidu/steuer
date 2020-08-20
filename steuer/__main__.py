"""
Steuer is a Selenium bot that fills invoices
for incorporated workers in São Paulo
"""
from time import sleep

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def has_valid_captcha(browser, expected_height=50, expected_width=180):
    """
    Checks if the login page has a valid captcha
    """
    # pylint: disable=line-too-long
    captcha = browser.find_element_by_xpath(
        "/html/body/div[1]/form/div[3]/div[5]/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/div/div[1]/img"
    )

    return captcha.size == {"height": expected_height, "width": expected_width}


def refresh_captcha(browser):
    """
    Refreshes the current captcha
    """
    refresh_btn = browser.find_element_by_id("btnAtualizar")
    refresh_btn.click()


def force_load_captcha(browser):
    """
    The login page sometimes fails to load a valid captcha. This function
    refreshes the captcha until a valid one appears
    """
    while not has_valid_captcha(browser):
        refresh_captcha(browser)
        sleep(1)


def login(cnpj, password, browser):
    """
    Logs the user in, but waits for a human-being to solve the captcha!
    """

    force_load_captcha(browser)

    pass_field = browser.find_element_by_id("ctl00_body_tbSenha")
    cnpj_field = browser.find_element_by_id("ctl00_body_tbCpfCnpj")
    login_btn = browser.find_element_by_id("ctl00_body_btEntrar")

    cnpj_field.send_keys(cnpj)
    pass_field.send_keys(password)

    WebDriverWait(browser, timeout=1000, poll_frequency=1).until(
        EC.staleness_of(login_btn)
    )


def open_emit_form(target, browser):
    """
    Opens the form to emit an invoice
    """
    open_emit_form_btn = browser.find_elements_by_link_text("Emissão de NFS-e")[0]
    open_emit_form_btn.click()

    target_select = Select(browser.find_element_by_id("ctl00_body_ddlApelido"))
    target_select.select_by_visible_text(target)

    next_btn = browser.find_element_by_id("ctl00_body_btAvancar")
    next_btn.click()


def fill_form(browser, value, description):
    """
    Fills the invoice form
    """
    description_field = browser.find_element_by_id("ctl00_body_tbDiscriminacao")
    description_field.send_keys(description)

    value_field = browser.find_element_by_id("ctl00_body_tbValor")
    value_field.send_keys(value)


def main(cnpj, password, target, value, description):
    """
    The main function. Basically it opens a selenium driver, logs the user in,
    opens the invoice form and fills it. The last step - actually emiting the
    invoice is left as a manual step for safety - not security - reasons.
    """

    browser = Firefox()

    browser.get("https://nfe.prefeitura.sp.gov.br")

    login(cnpj=cnpj, password=password, browser=browser)
    open_emit_form(target, browser)
    fill_form(browser, value, description)


if __name__ == "__main__":
    import argparse
    import os
    from pathlib import Path

    import dotenv

    # pylint: disable=invalid-name
    cli_description = (
        "Steuer gera nota fiscal da Prefeitura de SP pra você. "
        "Os campos cnpj, password, target e value podem ser configurados em secret.env"
    )

    env_path = Path(".") / "secret.env"
    dotenv.load_dotenv(dotenv_path=env_path)

    parser = argparse.ArgumentParser(description=cli_description)

    parser.add_argument(
        "--cnpj",
        default=os.getenv("cnpj"),
        help="O seu CNPJ, no formato xx.xxx.xxx/xxxx-xx",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("password"),
        help="A sua senha de login no site de emissão",
    )
    parser.add_argument(
        "--target",
        default=os.getenv("target"),
        help="O apelido do 'tomador de serviço' igual ao que você seleciona no menu de emissão",
    )
    parser.add_argument(
        "--value",
        default=os.getenv("value"),
        help="O valor da nota, no formato xxxx,xx",
    )

    parser.add_argument(
        "--description",
        default=os.getenv("description"),
        help="A descrição pra ser colocada na nota",
    )

    args = parser.parse_args()

    main(args.cnpj, args.password, args.target, args.value, args.description)

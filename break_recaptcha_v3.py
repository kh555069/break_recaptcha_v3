from requests import Session
import requests, json, re

def break_recaptcha_v3(site_key,co):
    req_session=Session()
    ### recaptcha anchor
    recaptcha_url = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k={}&co={}&hl=zh-TW&v=&size=invisible&cb='.format(site_key,co)
    resp = req_session.get(recaptcha_url)
    recaptcha_token = re.search(r'recaptcha-token.+?value="(.+?)"', resp.text).group(1)

    ### recaptcha reload
    payload = {"reason": "q", "c":recaptcha_token}
    reload_url = 'https://www.google.com/recaptcha/api2/reload?k={}'.format(site_key)
    resp = req_session.post(reload_url, data=payload)
    resp_json = resp.text.replace(')]}\'','').strip()
    token = json.loads(resp_json)[1]
    return token

if __name__=="__main__":
    from config.break_v3_config import site_key,co
    token = break_recaptcha_v3(site_key,co)
    url = 'http://localhost:5000/'
    d = {'g-recaptcha-response':token}
    print( requests.post(url,data=d).text )

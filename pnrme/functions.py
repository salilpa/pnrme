from pnrapi import pnrapi


def pnr_status_check(pnr_number, retries=3):
    """
    get the latest pnr status using pnrapi
    """
    pnr_status = pnrapi.PnrApi(pnr_number)
    if pnr_status.request():
        result = pnr_status.get_json()
        result['status'] = "Success"
        return result
    else:
        result = {
            "pnr": pnr_number
        }
        if pnr_status.error in ["Wrong PNR", "Circular Journey", "Train cancelled"]:
            result['status'] = "Permanent Error"
            result['error'] = pnr_status.error
            return result
        else:
            result['status'] = "Temporary Error"
            result['error'] = pnr_status.error
            if retries > 0:
                return pnr_status_check(pnr_number, retries-1)
            else:
                return result
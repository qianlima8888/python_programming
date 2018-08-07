import base64

def base_decode(url):
    #url = "b2Jmc3BhcmFtPSZyZW1hcmtzPVZFZnBvcEhwZ1pNNlFHOXVaWE56Y2cmZ3JvdXA9YjI1bGMzTnk"
    url = url + "==="
    return base64.b64decode(url)

def get_split(de_url, str):
    return de_url.split(str)
    
def decode_ss_url(ssurl):
    remark = "ss"
    port = ""
    method = ""
    ip_addr = ""
    password = ""
    timeout = 60
    if("#" in ssurl):
        remark = ssurl.split("#")[1]
        ssurl = ssurl.split("#")[0]
    
    if("@" in ssurl):
        p_m = get_split(ssurl.split("@")[1], ":")
        ip_addr = p_m[0]
        port = p_m[1]
        ssurl = ssurl.split("@")[0]
    
    de_url = str(base_decode(ssurl))[2:-2]
    if("@" in de_url):
        ip_addr, port = get_split(de_url.split("@")[1], ":")
        method, password = get_split(de_url.split("@")[0], ":")
    else:
        method, password = get_split(de_url, ":")
        
    print(remark, ip_addr, port, method, password)
    return [remark, ip_addr, port, method, password]

def decode_first(first):
    de_url =get_split(str(base_decode(first))[2:-2], ":");
    de_url[5] = str(base_decode(de_url[5]))[2:-2]
    print(de_url)
    return de_url

def decode_second(second):
    dic_url = {"obfsparam" : "", "protoparam" : "", "remarks" : "", "group" : ""}
    de_url =get_split(str(base_decode(second))[2:-2], "&");
    for strs in de_url:
        dic_url[strs.split("=")[0]] = str(base_decode(strs.split("=")[1]))[2:-2]
        print(base_decode(strs.split("=")[1]))
    de_url = [dic_url["obfsparam"], dic_url["protoparam"], dic_url["remarks"], dic_url["group"] ]
    print(de_url)
    return de_url

def decode_ssr_url(ssurl):
    ip_addr = ""
    port = ""
    protocol = ""
    method = ""
    obfs = ""
    password = ""
    obfsparam = ""
    protoparam = ""
    remarks = ""
    group = ""
    if("_" in ssurl):
        first = ssurl.split("_")[0]
        second = ssurl.split("_")[1]
        ip_addr, port , protocol, method, obfs, password = decode_first(first)
        obfsparam, protoparam, remarks, group = decode_second(second)
    
    print("end decode")


ssurl = input("input ss/ssr url:")
#ssurl = "ss://YWVzLTI1Ni1jZmI6aXN4Lnl0LTQzMTY3ODQ1QDE3OC4xMjguODQuMjUyOjE0NTU5@123.0.9.8:12345"
#ssurl = "ssr://NDUuNzcuMTg5LjExMTo0NDM6YXV0aF9hZXMxMjhfbWQ1OmFlcy0yNTYtY2ZiOnRsczEuMl90aWNrZXRfYXV0aDpiMjVsYzNOeS8_b2Jmc3BhcmFtPSZyZW1hcmtzPVZFZnBvcEhwZ1pNNlFHOXVaWE56Y2cmZ3JvdXA9YjI1bGMzTnk"
if("ss://" in ssurl):
    print("get ss url!\nstart decode.....")
    ssurl = ssurl[5:]
    decode_ss_url(ssurl)
    
elif("ssr://" in ssurl):
    print("get ssr url!\nstart decode.....")
    ssurl = ssurl[6:]
    decode_ssr_url(ssurl)
else:
    print("格式错误")

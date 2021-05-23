from fp.fp import FreeProxy
import myProxy
proxy = FreeProxy().get()
work = False
while work==False:
    work = myProxy.check_proxy(proxy)
    if work==False:
        proxy = FreeProxy().get()
# myProxy.check_proxy(proxy)
print(proxy)
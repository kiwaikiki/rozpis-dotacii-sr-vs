# Na načítanie dát sa odporúča použiť prílohu „zdroj_data23.xlsx“, v ktorej sa nachádzajú všetky relevantné premenné (počty zamestnancov, publikačné výkony, objemy grantov). Na výpočet regresných modelov sa odporúča štatistický program R, na načítanie dát je možné použiť napríklad knižnicu „readxl“:
install.packages("readxl")
# a privolať ju príkazom:
library(readxl)
# Za predpokladu, že príloha nazvaná „zdroj_data23.xlsx“ je uložená v priečinku s názvom R, dátový súbor sa načíta nasledovne:
dat = read.csv("//wsl.localhost/Ubuntu/home/viki/menezment/rozpis-dotacii-sr-vs/src/data.csv")
# Premenná „zam“ predstavuje počet zamestnancov v oblasti prírodných vied, premenná „pub“ predstavuje publikačné výkony daných pracovísk. Tieto premenné extrahujeme z dátového súboru pomocou príkazov:


zam = as.vector(dat$pocty_zamestnancov)
pub = as.vector(dat$publikacna_excelentnost)
# Pri vypočítaní iných modelov pre iné vedné oblasti je potrebné zmeniť názvy, a aj rešpektovať príslušný počet pracovísk (údaj v hranatých zátvorkách [1:24] zodpovedá počtu pracovísk v oblasti prírodných vied).
# Po nainštalovaní knižnice príkazom:
install.packages("gamlss")
# a jej privolaním príkazom


library(gamlss)
# je výpočet príslušného regresného modelu nasledovný:
m1 = gamlss(pub~offset(log(zam)), family=SICHEL, method=RS(200))
# Hodnoty, predikované modelom (popísané v bode 15 a uvedené v dátových prílohách) získame príkazom:
fitted(m1)
# Vypočítanú presnú hodnotu priemerného pomeru publikácií vidíme pomocou príkazu:
summary(m1)
# kde sa nachádza ako „Mu cofficients, Estimate“. Ak túto hodnotu prevedieme z logaritmickej škála príkazom exp(x), dostaneme pomer publikačných bodov na jedného zamestnanca.
# V prípade grantov, rovnako v súlade so štatistickou literatúrou, mali najlepšiu zhodu s údajmi modely, ktoré použili Tweedie distribúciu, zohľadňujúcu mimoriadnu šikmosť a veľký počet núl (Kurz, F. C. (2017): Tweedie distributions for fitting semicontinuous health care utilization cost data, BMC Medical Research Methodology, 17:171). Opäť autor presvedčivo ukázal, že kontinuálne premenné, ktoré sú mimoriadne šikmé, obsahujú extrémne hodnoty a excesívny počet núl (v bode 17 dodatok je zo zobrazení úplne zrejmé, že to platí aj pre objemy grantov), sa najlepšie modeluje pomocou Tweedie distrinúcie, ktorej pravdepodobnostná funkcia je nasledovná:
#  pričom jej parametre λ, α a β majú k distribučným parametrom μ, ϕ a p nasledujúci vzťah:

# Na výpočet sa použila knižnica „glmmTMB“, jej inštalácia a privolanie:
install.packages("glmmTMB")
# a privolá sa príkazom:
library(glmmTMB)
# Za predpokladu, že si pripravíme premennú s grantovými výkonmi:
gra = as.vector(dat$sum_granty)
# príslušný model sa vypočíta nasledovne:
m2 = glmmTMB(gra~offset(log(zam)), family=tweedie)
# Vypočítanú presnú hodnotu priemerného pomeru grantového objemu vidíme pomocou príkazu:
summary(m2)
# kde sa nachádza ako „Conditional model, Estimate“. Ak túto hodnotu prevedieme z logaritmickej škála príkazom exp(x), dostaneme pomer grantového objemu na jedného zamestnanca.

dat$rezidua_granty = gra - exp(predict(m2, data = zam))

dat$rezidua_publ = pub - exp(predict(m1, data = zam))


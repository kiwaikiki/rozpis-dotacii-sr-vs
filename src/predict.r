options(HTTPUserAgent = sprintf("R/%s R (%s)", getRversion(), paste(getRversion(), R.version["platform"], R.version["arch"], R.version["os"])))
options(repos = c(CRAN = "https://cloud.r-project.org/"))
# install.packages(c("gamlss", "glmmTMB"))

ALL = TRUE
path_prefix = "../data/"

# function which trains models
train_model = function(dat, oblast) {
    # Premenná „zam“ predstavuje počet zamestnancov v oblasti prírodných vied, premenná „pub“ predstavuje publikačné výkony daných pracovísk. Tieto premenné extrahujeme z dátového súboru pomocou príkazov:
    zam = as.vector(dat$pocty_zamestnancov)
    pub = as.vector(dat$publikacna_excelentnost)
    gra = as.vector(dat$sum_granty)
    zam
    pub
    gra

    library(gamlss)
    m1 = gamlss(pub~offset(log(zam)), family=SICHEL, method=RS(200))
    # Hodnoty, predikované modelom (popísané v bode 15 a uvedené v dátových prílohách) získame príkazom:
    fitted(m1)
    # Vypočítanú presnú hodnotu priemerného pomeru publikácií vidíme pomocou príkazu:
    summary(m1)
    # kde sa nachádza ako „Mu cofficients, Estimate“. Ak túto hodnotu prevedieme z logaritmickej škála príkazom exp(x), dostaneme pomer publikačných bodov na jedného zamestnanca.
    # V prípade grantov, rovnako v súlade so štatistickou literatúrou, mali najlepšiu zhodu s údajmi modely, ktoré použili Tweedie distribúciu, zohľadňujúcu mimoriadnu šikmosť a veľký počet núl (Kurz, F. C. (2017): Tweedie distributions for fitting semicontinuous health care utilization cost data, BMC Medical Research Methodology, 17:171). Opäť autor presvedčivo ukázal, že kontinuálne premenné, ktoré sú mimoriadne šikmé, obsahujú extrémne hodnoty a excesívny počet núl (v bode 17 dodatok je zo zobrazení úplne zrejmé, že to platí aj pre objemy grantov), sa najlepšie modeluje pomocou Tweedie distrinúcie, ktorej pravdepodobnostná funkcia je nasledovná:
    #  pričom jej parametre λ, α a β majú k distribučným parametrom μ, ϕ a p nasledujúci vzťah:

    library(glmmTMB)
    m2 = glmmTMB(gra~offset(log(zam)), family=tweedie)
    # Vypočítanú presnú hodnotu priemerného pomeru grantového objemu vidíme pomocou príkazu:
    summary(m2)
    # kde sa nachádza ako „Conditional model, Estimate“. Ak túto hodnotu prevedieme z logaritmickej škála príkazom exp(x), dostaneme pomer grantového objemu na jedného zamestnanca.

    dat$rezidua_granty = gra - exp(predict(m2, data = zam))
    dat$rezidua_publ = pub - exp(predict(m1, data = zam))
    write.csv(dat, file = paste(path_prefix, "predict_", oblast, ".csv", sep=""))
}

if (ALL) {
    for (i in 1:6) {
        oblast = paste("M", i, sep="")
        dat = read.csv(paste(path_prefix, "data_", oblast, ".csv", sep=""))
        train_model(dat, oblast)
    }
} else {
    dat = read.csv(paste(path_prefix, "data_", ".csv", sep=""))
    train_model(dat, "")
}

function () {
    window.getArenaCookie = function getArenaCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(window.document.cookie);
        let ca = decodedCookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
            c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    window.setArenaCookie = function setArenaCookie(cname, cvalue, exdays) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toUTCString();
        window.document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    if (window.getArenaCookie('session').length == 0)
    {
        const d = new Date();
        window.setArenaCookie('session', d.getTime().toString(), 90);
        console.log('Session cookie created')
    }
}
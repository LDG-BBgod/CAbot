function OpenMenu() {
    document.getElementsByClassName('menuGroup')[0].classList.add('on')
    document.getElementsByClassName('menuBar')[0].classList.add('off')
    document.getElementsByClassName('menuX')[0].classList.add('on')
}


function CloseMenu() {
    document.getElementsByClassName('menuGroup')[0].classList.remove('on')
    document.getElementsByClassName('menuBar')[0].classList.remove('off')
    document.getElementsByClassName('menuX')[0].classList.remove('on')
}

window.addEventListener('resize', () => {

    if (window.innerWidth > 600) {
        document.getElementsByClassName('menuGroup')[0].classList.remove('on')
        document.getElementsByClassName('menuBar')[0].classList.remove('off')
        document.getElementsByClassName('menuX')[0].classList.remove('on')
        try {
            document.getElementById('section3Imgs').style.marginLeft = '0'
        }
        catch {}
    }
})
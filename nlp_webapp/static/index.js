function show_up(show) {
    document.getElementById(show).style.display="block";
  } 

const showVSA = document.querySelector('#show_VSA');
const showSC = document.querySelector('#show_SC');
const divs_9 = document.querySelectorAll('.column.is-9');
const bt = document.getElementById('button_right');

function hideAll() {
    for (const div of divs_9) {
        div.style.display = 'none';
    }
}

showVSA.addEventListener('click', () => {
    hideAll();
    dVSA = document.getElementById('div_VSA');
    dVSA.style.display = 'block';
    bt.style.display = 'block';
});

showSC.addEventListener('click', () => {
    hideAll();
    dSC = document.getElementById('div_SC');
    dSC.style.display = 'block';
    bt.style.display = 'block';
});  
  
  
  
  
  

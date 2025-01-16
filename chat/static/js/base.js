function adjustZoom() {
    const width = window.innerWidth;
    // TODO: uncommment and update logic below to adjust zoom level based on screen width
    // requirements not clear, so I'm not sure what to do here

    // if (width <= 600) {
    //   document.body.style.transform = "scale(0.5)";
    // } else if (width <= 700) {
    //   document.body.style.transform = "scale(0.75)";
    // } else if (width <= 767) {
    //   document.body.style.transform = "scale(0.8)";
    // } else if (width <= 1200) {
    //   document.body.style.transform = "scale(0.9)";
    // } else {
    //   document.body.style.transform = "scale(1)";
    // }
    sidebarRespond();
}

function sidebarRespond() {
  const width = window.innerWidth; 
  if (width <= 1200) {
    collapseSidebar();
    document.querySelector('#right-panel').classList.add('hidden');
  }else{
    expandSidebar();
    document.querySelector('#right-panel').classList.remove('hidden');
  }
}

  window.addEventListener("resize", adjustZoom);
  adjustZoom();
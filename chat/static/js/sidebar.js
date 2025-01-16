function collapseSidebar() {
    const sidebar = document.querySelector('#sidebar');
    const usersH2 = sidebar.querySelector('h2');
    const usersContainer = document.querySelector('#users-container');
    const mainContainer = document.querySelector('main');

    sidebar.classList.remove('sidebar-expanded');
    sidebar.classList.add('sidebar-collapsed');
    usersH2.classList.add('hidden');
    if(usersContainer) usersContainer.classList.add('collapsed');
    mainContainer.style.marginLeft = '70px';
    
}

function expandSidebar() {
    const sidebar = document.querySelector('#sidebar');
    const usersH2 = sidebar.querySelector('h2');
    const usersContainer = document.querySelector('#users-container');
    const mainContainer = document.querySelector('main');

    sidebar.classList.remove('sidebar-collapsed');
    sidebar.classList.add('sidebar-expanded');
    usersH2.classList.remove('hidden');
    if(usersContainer) usersContainer.classList.remove('collapsed');
    mainContainer.style.marginLeft = '20%';
}

function toggleSidebar() {
    const sidebar = document.querySelector('#sidebar');

    const isExpanded = sidebar.classList.contains('sidebar-expanded');
    if(isExpanded) {
        collapseSidebar();
    } else {
        expandSidebar();
    }        
}
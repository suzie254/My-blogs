document.addEventListener('DOMContentLoaded', function() {
    var options = {};
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, options);
});

document.addEventListener('DOMContentLoaded', function() {
    var options = {'coverTrigger': false};
    var dropelems = document.querySelectorAll('.dropdown-trigger');
    var dropinstances = M.Dropdown.init(dropelems, options);
});
function change_username() {
    var change_username = document.getElementById('account_username')
    if (change_username.readOnly) {
        change_username.readOnly = false
    } else {
        change_username.readOnly = true
    }
}


function change_goal() {
    var change_goal = document.getElementById('account_study_time')
    if (change_goal.readOnly) {
        change_goal.readOnly = false
    } else {
        change_goal.readOnly = true
    }
}
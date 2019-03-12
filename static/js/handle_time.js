function deal_with_time() {
    let time = new Date();
    year = time.getFullYear();
    month = time.getMonth();
    date = time.getDate();
    hour = time.getHours();
    minute = time.getMinutes();
    second = time.getMinutes();
    finally_time_form = year + ":" + month + ":" + date + ":" + hour + ":" + minute + ":" + second;
    return finally_time_form
}
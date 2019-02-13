'use strict';

$(document).ready(function () {
    $('body').keypress(function (e) {
        if (e.keyCode == 32) {
            $('#btn-play').click();
        }
    });
});

function ajax(url, successFunc) {
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function (resp) {
            console.log(resp);
            successFunc(resp);
        },
        error: function (resp) {
            console.log(resp);
        }
    });
}

class Player {
    constructor(playlist, seek_bar_id, fill_bar_id, prev_id, next_id, static_url, button_play, div_name, loading, pl_time, bar_volume, label) {
        this.playlist = playlist;
        this.seek = $('#' + seek_bar_id)[0];
        this.fill = $('#' + fill_bar_id)[0];
        this.prev_btn = $('#' + prev_id)[0];
        this.next_btn = $('#' + next_id)[0];
        this.btn_play = $('#' + button_play)[0];
        this.widget_name = $('#' + div_name)[0];
        this.loader = $('#' + loading)[0];
        this.div_time = $('#' + pl_time)[0];
        this.volume_bar = $('#' + bar_volume)[0];
        this.volume_label = $('#' + label)[0];
        this.volume_seek = this.volume_bar.childNodes[3];
        this.volume_fill = this.volume_seek.childNodes[1];
        this.prev_btn.onclick = () => this.prev(this);
        this.next_btn.onclick = () => this.next(this);
        this.url = static_url;
        this.current = 0;
        this.move_seek = false;
        this.audio = new Audio();
        this.audio.onended = () => this.next(this);
        this.audio.addEventListener("timeupdate", () => this.updateSeek(this));
        this.audio.addEventListener("progress", (e) => this.updateLoading(e, this));
        this.audio.addEventListener("loadeddata", (e) => this.updateLoading(e, this));
        this.seek.addEventListener("mousedown", (e) => this.mouseDownSeek(e, this));
        this.seek.addEventListener("mouseover", (e) => this.timeBlockMouseover(e, this));
        this.seek.addEventListener("mousemove", (e) => this.timeBlockMouseover(e, this));
        $(this.volume_seek).mousedown((e) => {
            if (e.target.id !== "handle-volume")
                this.set_volume((e.target.offsetHeight - e.offsetY) / this.volume_seek.offsetHeight * 100);
            this.volume_bar.onmousemove = (e) => {
                let temp = 0;
                if (!["handle-volume", "label-volume-bar"].includes(e.target.id)) {
                    temp = Math.abs(e.target.offsetHeight - e.offsetY - $('#handle-volume')[0].offsetHeight) / this.volume_seek.offsetHeight * 100;
                } else {
                    let t = e.movementY / this.volume_seek.offsetHeight * 100 * -1,
                        last = parseFloat(this.volume_fill.style.height);
                    temp = last + t;
                }
                this.set_volume(temp);
            };
            $(this.volume_bar).mouseup((e) => {
                this.volume_bar.onmousemove = null;
            });
        });
        this.timer = 0;
        this.last_dur = 0;
    }

    set_volume(vol) {
        vol = Math.max(Math.min(vol, 100), 0);
        this.volume_fill.style.height = vol + "%";
        this.audio.volume = vol / 100;
        this.volume_label.innerText = Math.round(vol);
        if (vol >= 75) vol = 75;
        else if (vol >= 25) vol = 50;
        else if (vol > 0) vol = 25;
        else vol = 0;
        $("#sound-scroll-button")[0].classList.forEach((value, i) => {
            if (value.includes("icon-volume-"))
                $("#sound-scroll-button")[0].classList.replace(value, "icon-volume-" + vol);
        });
    }

    show_hide_volume(e) {
        if (this.volume_bar.style.display === "block")
            this.volume_bar.style.display = "none";
        else {
            this.volume_bar.style.display = "block";
            $(this.volume_bar).mouseleave((e) => {
                this.volume_bar.style.display = "none";
                this.volume_bar.onmousemove = null;
            });
        }
    }

    timeBlockMouseover(e, pl) {
        //console.log(e);
        let time = Math.round(+e['offsetX'] / pl.seek.offsetWidth * pl.playlist.results[this.current]['podcast']['duration']);
        pl.div_time.innerText = this.timetoString(time);
        pl.div_time.style.left = (e['offsetX'] - pl.div_time.offsetWidth / 2) / pl.seek.offsetWidth * 100 + "%";
    }

    timetoString(s) {
        s |= 0;
        let time = [s % 60];
        let min = s / 60 | 0;
        if (min >= 60) {
            time.push(min % 60);
            time.push(min / 60 | 0);
        } else time.push(min);
        time.reverse();
        for (let i = time.length - 1; i >= +(time.length > 2); i--)
            if (time[i] < 10) time[i] = "0" + time[i].toString();
        return time.length > 1 ? time.join(":") : "00:" + time.join(":");
    }

    play_pause(event) {
        if (this.audio.paused) {
            if (!this.audio.src) this.changeAudio();
            else this.audio.play();
            event.srcElement.classList.replace("icon-play", "icon-pause");
        } else {
            this.audio.pause();
            event.srcElement.classList.replace("icon-pause", "icon-play");
        }
    }

    updateLoading(e, pl = this) {
        pl.loader.style.width = e.path[0].buffered.end(0) / pl.audio.duration * 100 + "%";
        //console.log("Length: " + e.path[0].buffered.length + " | " + e.path[0].buffered.start(0) + " | " + e.path[0].buffered.end(0));
    }

    preload_nextPage() {
        if (this.playlist.next) {
            ajax(this.playlist.next, (resp) => {
                resp.results = this.playlist.results.concat(resp.results);
                this.playlist = resp;
            });
        }
    }

    mouseDownSeek(e, pl) {
        //console.log(e);
        pl.move_seek = true;
        pl.fill.style.width = Math.abs(e['offsetX']) / pl.seek.offsetWidth * 100 + "%";
        document.body.onmousemove = (e) => pl.mouseMove(e, pl);
        document.body.onmouseup = () => pl.mouseUp(pl);
    }

    updateSeek(pl = this) {
        if (!pl.move_seek) {
            let position = pl.audio.currentTime / pl.audio.duration;
            pl.fill.style.width = position * 100 + '%';

        }
        $("#play-time-left")[0].innerText = pl.timetoString(pl.audio.currentTime);
        $("#play-time-right")[0].innerText = "-" + pl.timetoString(pl.audio.duration - pl.audio.currentTime);
        let temp = pl.audio.currentTime - pl.last_dur;
        if (temp < 2 && temp > 0)
            pl.timer += temp;
        pl.last_dur = pl.audio.currentTime;
        if (pl.timer >= 15) {
            Player.listened_n(pl.playlist.results[pl.current].id);
            pl.timer = 0;
        }
    }

    static listened_n(id, n = 15) {
        $.ajax({
            url: `/channels/api/user_podcasts/${id}/listened_n/`,
            headers: {
                'X-CSRFTOKEN': token
            },
            type: 'PATCH',
            dataType: 'json',
            data: {'listen': n},
            success: function (resp) {
                //console.log(resp);
            },
            error: function (resp) {
                console.log(resp);
            }
        });
    }

    changeTimebyVector(v = 0) {
        if (this.audio.currentTime + v > this.audio.duration)
            this.next();
        else if (this.audio.currentTime + v < 0) {
            if (this.audio.currentTime < 1) this.prev();
            else this.audio.currentTime = 0;
        } else this.audio.currentTime += v;
    }

    playID(id) {
        if (id < this.playlist.results.length) {
            this.current = id;
            this.changeAudio();
        }
    }

    changeAudio(v = 0) {
        if (this.playlist.results < 1) return false;
        if (this.timer > 5) {
            Player.listened_n(this.playlist.results[this.current].id, Math.round(this.timer));
            this.timer = 0;
        }
        let i = 0;
        do {
            if (i > this.playlist.results.length * 2) return false;
            this.current += v;
            if (this.current + 2 >= this.playlist.results.length) this.preload_nextPage();
            if (this.current < 0) this.current = this.playlist.results.length - 1;
            if (this.current >= this.playlist.results.length) this.current = 0;
            if (v === 0) v = 1;
            i++;
        } while (!this.playlist.results[this.current]['podcast']['processed']);
        this.audio.pause();
        this.audio.src = this.url + this.playlist.results[this.current]['podcast']['video_id'] + ".mp3";
        this.widget_name.innerText = this.playlist.results[this.current]['podcast']['name'];
        this.audio.play();
        this.fill.style.width = "0%";
        this.btn_play.classList.replace("icon-play", "icon-pause");
        document.title = this.playlist.results[this.current]['podcast']['name'];
        //$("#icon")[0].href = this.playlist.results[this.current]['podcast']['thumbnails_url'];
        setWatched(this.playlist.results[this.current].id);
        return true;
    }

    next(pl = this) {
        pl.changeAudio(1);
    }

    prev(pl = this) {
        pl.changeAudio(-1);
    }

    static calc_offsetLefts(node) {
        let left = 0, last = 0;
        while (node.tagName !== "BODY") {
            left += node.offsetLeft;
            last = node.offsetLeft ? node.offsetLeft : last;
            node = node.parentElement;
        }
        return left - last;
    }

    mouseMove(event, pl) {
        //console.log(event);
        let temp = (event['clientX'] - Player.calc_offsetLefts(pl.seek.parentElement)) / pl.seek.offsetWidth * 100;
        if (temp > 100) temp = 100;
        if (temp < 0) temp = 0;
        pl.fill.style.width = temp + '%';
    }

    mouseUp(pl) {
        if (pl.move_seek) {
            document.body.onmousemove = null;
            document.body.onmouseup = null;
            //console.log(parseFloat(pl.fill.style.width));
            pl.audio.currentTime = pl.audio.duration / 100 * parseFloat(pl.fill.style.width);
            pl.move_seek = false;
        }
    }
}

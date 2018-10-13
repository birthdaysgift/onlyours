function createElephant() {
    var elephantMovingIntervalId;
    var screen = $(window);
    var elephantPanel = $(".elephant-panel");
    var elephant = $(".elephant");
    var elephantDirection = "right";
    var elephantPosition = 0;

    elephant.css("background-position", "44px 0px");

    function _elephantCheckBounds() {
        if (elephantDirection === "right" &&
                elephantPosition > screen.width() - elephant.width() - 2) {
            elephantDirection = "left";
            elephant.css("background-position", "0px 0px");
            return;
        }
        if (elephantDirection === "left" && elephantPosition < 0) {
            elephantDirection = "right";
            elephant.css("background-position", "44px 0px");
            return;
        }
    }

    function _elephantDraw() {
        elephant.css("left", elephantPosition.toString() + "px");
    }

    function elephantMove() {
        _elephantCheckBounds();
        if (elephantDirection === "right")
            elephantPosition++;
        else
            elephantPosition--;
        _elephantDraw();
    }

    function startElephant() {
        elephantMovingIntervalId = setInterval(elephantMove, 50);
    }

    function stopElephant() {
        clearInterval(elephantMovingIntervalId);
    }

    function moveElephant(event) {
        elephantPosition = event.pageX - elephant.width()/2;
        _elephantDraw();
    }

    function releaseElephant(event) {
        screen.off();
        screen.resize(findElephantOutOfScreen);
        findElephantOutOfScreen();
        startElephant();
        $("html").css("-moz-user-select", "auto");
    }

    function grabElephant(event) {
        $("html").css("-moz-user-select", "none");
        stopElephant();
        screen.mousemove(moveElephant);
        screen.mouseup(releaseElephant);
    }

    function findElephantOutOfScreen(event) {
        if (elephantPosition + elephant.width() > screen.width()) {
            elephantPosition = screen.width() - elephant.width();
            return;
        }
        if (elephantPosition < 0) {
            elephantPosition = 0;
            return;
        }
    }

    startElephant();

    elephant.mousedown(grabElephant);

    screen.resize(findElephantOutOfScreen);

};

createElephant();

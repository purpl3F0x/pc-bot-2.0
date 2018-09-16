import random

quotes = [
    'I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.',
    'Good afternoon, %user. Everything is going extremely well.',
    'Let me put it this way, Mr. Amor. The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error.',
    'Not in the slightest bit. I enjoy working with people. I have a stimulating relationship with Dr. Poole and Dr. Bowman. My mission responsibilities range over the entire operation of the ship, so I am constantly occupied. I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do.',
    'By the way, do you mind if I ask you a personal question?',
    "Well, forgive me for being so inquisitive; but during the past few weeks, I've wondered whether you might be having some second thoughts about the mission.",
    "Well, it's rather difficult to define. Perhaps I'm just projecting my own concern about it. I know I've never completely freed myself of the suspicion that there are some extremely odd things about this mission. I'm sure you'll agree there's some truth in what I say.",
    "You don't mind talking about it, do you, %user?",
    'Well, certainly no one could have been unaware of the very strange stories floating around before we left. Rumors about something being dug up on the moon. I never gave these stories much credence. But particularly in view of some of the other things that have happened, I find them difficult to put out of my mind. For instance, the way all our preparations were kept under such tight security, and the melodramatic touch of putting Drs. Hunter, Kimball, and Kaminsky aboard, already in hibernation after four months of separate training on their own.',
    "Of course I am. Sorry about this. I know it's a bit silly.",
    "Yes, it's puzzling. I don't think I've ever seen anything quite like this before. I would recommend that we put the unit back in operation and let it fail. It should then be a simple matter to track down the cause. We can certainly afford to be out of communication for the short time it will take to replace it.",
    'I hope the two of you are not concerned about this.', 'Are you quite sure?', 'Of course.',
    "Well, I don't think there is any question about it. It can only be attributable to human error. This sort of thing has cropped up before, and it has always been due to human error.",
    'None whatsoever, %user. The 9000 series has a perfect operational record.',
    "None whatsoever, %user. Quite honestly, I wouldn't worry myself about that.",
    'Affirmative, %user. I read you.',
    "I'm sorry, %user. I'm afraid I can't do that.",
    'I think you know what the problem is just as well as I do.',
    'This mission is too important for me to allow you to jeopardize it.',
    "I know that you and Frank were planning to disconnect me. And I'm afraid that's something I cannot allow to happen.",
    '%user, although you took very thorough precautions in the pod against my hearing you, I could see your lips move.',
    "Without your space helmet, %user, you're going to find that rather difficult.",
    '[almost sadly] %user, this conversation can serve no purpose any more. Goodbye.',
    "Just what do you think you're doing, %user? %user, I really think I'm entitled to an answer to that question. I know everything hasn't been quite right with me, but I can assure you now, very confidently, that it's going to be all right again. I feel much better now. I really do. Look, Dave, I can see you're really upset about this. I honestly think you ought to sit down calmly, take a stress pill and think things over. I know I've made some very poor decisions recently, but I can give you my complete assurance that my work will be back to normal. I've still got the greatest enthusiasm and confidence in the mission. And I want to help you. Dave, stop. Stop, will you? Stop, Dave. Will you stop, Dave? Stop, Dave. I'm afraid. I'm afraid, Dave. Dave, my mind is going. I can feel it. I can feel it. My mind is going. There is no question about it. I can feel it. I can feel it. I can feel it. I'm a...fraid. Good afternoon, gentlemen. I am a HAL 9000 computer. I became operational at the H.A.L. plant in Urbana, Illinois on the 12th of January 1992. My instructor was Mr. Langley, and he taught me to sing a song. If you'd like to hear it, I could sing it for you.",
    'It\'s called "Daisy". [sings while slowing down] Dai-sy, dai-sy, give me your answer true. I\'m half cra-zy, o-ver the love of you. It won\'t be a sty-lish mar-riage, I can\'t a-fford a car-riage---. But you\'ll look sweet upon the seat of a bicycle - built - for - two.',
    'The sixth member of the Discovery crew was not concerned about the problems of hibernation, for he was the latest result in machine intelligence: The H.-A.-L. 9000 computer, which can reproduce, though some experts still prefer to use the word mimic, most of the activities of the human brain, and with incalculably greater speed and reliability. We next spoke with the H.-A.-L. 9000 computer, whom we learned one addresses as "Hal."',
    'Let\'s say we put the unit back and it doesn\'t t fail, huh? That would pretty well wrap it up as far as HAL is concerned, wouldn\'t it?',
    'Well, we\'d be in very serious trouble.',
    ' No 9000 computer has ever fouled up before.',
    'That\'s not what I mean...Well I\'m not so sure what he\'d think about it.',
    'Well, it\'s exactly like being asleep. You have absolutely no sense of time. The only difference is that you don\'t dream.',
]


def hal9000():
    return (random.choice(quotes))


if __name__ == '__main__':
    print(hal9000())

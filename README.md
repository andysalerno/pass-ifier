# pass-ifier
Python tool for generating strong, yet still humanly memorable, passwords that can be deterministically regenerated at any time.

# Example:  
    $ python3 Passifier.py  
    Enter master password:  
    Site name (case insensitive): facebook
    number to recalc a password, or enter to calc new one:  
    Your password: NovelsSunwardsPeacefulness:93  
    happy? (if no, will reroll) y/n: n  
    Your password: ScalpingAquiferGimmickry:37  
    happy? (if no, will reroll) y/n: n  
    Your password: CamembertSplashersColonials:71  
    happy? (if no, will reroll) y/n: n  
    Your password: PerusalGrimyGenteelest:96  
    happy? (if no, will reroll) y/n: n  
    Your password: UnfeltDestructivenessAnodizing:50  
    happy? (if no, will reroll) y/n: n  
    Your password: HelicoptsCrapedReiterated:5  
    happy? (if no, will reroll) y/n: n  
    Your password: AdulterousTrottingVotable:66  
    happy? (if no, will reroll) y/n: n  
    Your password: PreacceptanceJanitorialCasteless:46  
    happy? (if no, will reroll) y/n: n  
    Your password: GluttingInterrelatednessQuietest:44  
    happy? (if no, will reroll) y/n: n  
    Your password: CressetsAlgorismMeta:55  
    happy? (if no, will reroll) y/n: y  
    
Recomputing a password you forgot:

    $ python3 Passifier.py
    Enter master password:
    Site name (case insensitive): facebook
    number to recalc a password, or enter to calc new one: 55
    Your password: CressetsAlgorismMeta:55



# What's a deterministic password generator?
Feel free to skip to the next section if you already know this.  
A deterministic password generator is one that doesn't *store* your passwords anywhere. 
This means there is no cloud service, not even a local database that could be compromised. All the information
you need is in your head.

To generate the password, you give it a master password and the website's name.  The combination
is hashed with SHA256, along with a random number.  The resulting hash is used to pick words out of an English
dictionary, resulting in a password that's much easier to remember than a hex string.

If you ever forget your password, you just type in your master password and website name again,
along with the number it told you, and it will recalculate the same password, without needing to store
it anywhere.

# Deterministically generate passwords for humans
Other password generators give you long hash values in hex that you will never remember.  
This password generator uses an English dictionary to spit out passwords comprised of English words.

Here are some passwords created by this generator:  
SkidooedDietsDilemma:96  
MortalPsychosesMetatarsally:68  
RetoolExcessivelyBaby:93

With three English words and one number 0-99, there are (109582^3) * 100 = 1.3158842e+17 permutations.

In future versions, the amount of words and the amount of number possibilities might become configurable.

There's currently no implementation to specify other characters, such as exclamation marks.  I think that would require the user
to remember too much.  So far, most websites I use accept this format, as it has capital letters, a symbol ':', and a number.

# Things to implement/fix
* Consider allowing the user the ability to increase/decrease the entropy of the output, by allowing more words or characters
* Switch from SHA256 to scrypt or bcrypt.
* Perhaps switch to a dictionary of more common words, and increase word count to 4, a la XKCD?
* Make the prompt and printed statements less ugly.

# Disclamer
Don't take medical advice from anyone besides your doctor, legal advice from anyone besides your lawyer, or cryptographic advice from anyone besides your cryptographer.
This tool is a project made for fun.  I myself use it, but I'm not Snowden, and there may be flaws in its design or concept.

# Questions

1. blue vs red? is it simply about classifying red part vs blue part? or is it just that the only colours parts have are blue and red?
2. is there any data already available?
3. how fast conveyor is moving? no change of speed?
4. the conveyor is moving 24h/7? the vision system should work 24h/7
5. what does changer de référence produit mean?

# plan

we want to know what parts are on the conveyor (classification) and where there are (detection)

requirements:
• Le robot aura besoin d’une position exploitable pour saisir les pièces
• Le client demande une précision de ±0,1 mm

I understand that the robot has to seize the parts
I understand that the robot can successfully seize a part only if it seizes it at specific location
I understand the allowed error of locating those specific locations is ±0,1 mm

This error can be translated into a pixel error and thus an estimation of the minimal image resolution can be made

assumption:
    - camera is at 1 meter from the part

for a $1024 \times 1024$ pixels image, considering a part at a distance of 1 meter
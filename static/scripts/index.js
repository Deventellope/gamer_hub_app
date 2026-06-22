
element= document.getElementById("game_card")
container= element.parentElement


for(let i=0; i<7 ; i+=1){
        paths= ["static\\images\\Cute Spongebob Wallpaper HD.jfif",
"static\\images\\1142647736720861356.jfif",
"static\\images\\Epic 4K Anime Wallpapers 🔥 _ HD Action & Fantasy Backgrounds Description_ Epic anime wallpapers in.jfif",
"static\\images\\910501249688650479.jfif",
"static\\images\\1142647736720861356.jfif",
"static\\images\\Spider-Man.jfif"

    ]

    path= paths[ Math.floor(Math.random() * paths.length ) ]

    cloned= element.cloneNode(true)

    cloned.getElementsByTagName("img")[0].src= path

    container.appendChild(cloned)
    console.log("new element appended".toUpperCase())
}


a_element= document.getElementById("trend_card")
a_container= a_element.parentElement


for(let i=0; i<15 ; i+=1){
    paths= ["static\\images\\Cute Spongebob Wallpaper HD.jfif",
"static\\images\\1142647736720861356.jfif",
"static\\images\\Epic 4K Anime Wallpapers 🔥 _ HD Action & Fantasy Backgrounds Description_ Epic anime wallpapers in.jfif",
"static\\images\\910501249688650479.jfif"
    ]

    path= paths[ Math.floor(Math.random() * paths.length ) ]

    cloned= a_element.cloneNode(true) 
    cloned_img= cloned.getElementsByTagName("img")
    cloned_img[0].src= path

    a_container.appendChild(cloned)
        
    console.log("new trending card element appended".toUpperCase())
}
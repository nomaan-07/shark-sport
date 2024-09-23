/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.{html,js}"],
  theme: {
    extend: {
      container:{
        center: true,
        padding:{
          DEFAULT : "1rem", // 16px
          lg : "4.375rem", // 70px
        }
      },
      colors:{
        blueBrand : "#4455E8",
        orangeBrand : "#FF9447",
        orangeTint_1 : "#FFDEC7",
        orangeTint_3 : "#F29F64",
        grayTint_1 : "#E6E6E6",
        grayTint_2 : "#CCC",
        grayTint_3 : "#B3B3B3",
        grayTint_4 : "#999999",
        grayShade_1 : "#666666",
        overlayBcg : "#00000066",
        neutralBorder : "#E0E0E2",
      },
      backgroundImage : {
        "custom-gradient" : 'linear-gradient(180deg, rgba(33, 33, 33, 0.53) 53%, #212121 100%)',
        "custom-gradient2" : 'linear-gradient(180deg, rgba(33, 33, 33, 0.53) 100%, #212121 53%)',
        "custom-gradient3" : 'linear-gradient(90deg, rgba(243, 67, 67, 0.58) 0%, #F64F77 100%)',
      },
      fontFamily : {
        "vazir" : "Vazir",
        "vazirLight" : "Vazir Light",
        "vazirMedium": "Vazir Medium",
        "vazirBold" : "Vazir Bold",
        "vazirblack" : "Vazir black",
      },
      dropShadow : {
        "bannerTitle" : "0 5px .6px rgba(0,0,0,.25)"
      },
      fontSize: {
        '32': '2rem',
      },
    },
    screens :{
      'xs': '576px',
      'sm': '768px',
      'md': '992px',
      'lg': '1200px',
      'xl': '1400px',
    },
  },
  plugins: [],
}

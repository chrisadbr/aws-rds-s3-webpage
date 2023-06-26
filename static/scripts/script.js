const getSurveyForm = (e) => {
    const surveyContainer = document.querySelector('.survey__container')
    surveyContainer.classList.toggle('active')
    console.log(surveyContainer)
}
const closeForm = (e) => {
    const surveyContainer = document.querySelector('.survey__container')
    surveyContainer.classList.toggle('active')
    console.log(surveyContainer)
}
const openForm = (e) => {
    const surveyContainer = document.querySelector('.survey__container')
    console.log(`Here: ${surveyContainer}`)
}
//
const sendForm = (e) => {
    const surveyContainer = document.querySelector('.survey__container')
    alert('surveyContainer')
}
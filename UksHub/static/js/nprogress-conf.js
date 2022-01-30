NProgress.configure({
  showSpinner: false
});
window.addEventListener('beforeunload', () => {
  NProgress.start();
})

window.addEventListener('unload', () => {
  NProgress.done(True);
})
function initializeToolTips() {
  const toolTipElements = document.querySelectorAll('.toolTip');
  console.log(toolTipElements)
  toolTipElements.forEach((toolTip) => {
    console.log(toolTip)
    const message = toolTip.getAttribute('data-tool-tip-message');
    const toolTipContainer = toolTip.getAttribute('data-tool-tip-container');
    const toolTipMessageContainer = toolTip.getAttribute('data-tool-tip-message-container');
    console.log(toolTipContainer)
    const toolTipTarget = document.getElementById(toolTipContainer);
    const toolTipTarget_paragraph = document.getElementById(toolTipMessageContainer);
    toolTip.addEventListener('mouseover', () => {
      toolTipTarget_paragraph.innerText = message;
      toolTipTarget.classList.add('active');
    });

    toolTip.addEventListener('mouseout', () => {
      toolTipTarget.classList.remove('active');
    });


  });
}

export {initializeToolTips};
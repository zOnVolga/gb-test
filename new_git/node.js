function generateOctoberCalendar(year) {
    const daysOfWeek = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
    const octoberCalendar = [];
    
    for (let day = 1; day <= 31; day++) {
        const date = new Date(year, 9, day); // Месяцы в JavaScript начинаются с 0, поэтому октябрь - это 9
        const dayOfWeek = daysOfWeek[date.getDay()];
        const isWeekend = (dayOfWeek === "Суббота" || dayOfWeek === "Воскресенье");
        
        octoberCalendar.push({
            date: `${year}-10-${String(day).padStart(2, '0')}`,
            dayOfWeek: dayOfWeek,
            isWeekend: isWeekend
        });
    }
    
    return octoberCalendar;
}

// Пример использования
const octoberCalendar = generateOctoberCalendar(2023);
console.log(octoberCalendar);

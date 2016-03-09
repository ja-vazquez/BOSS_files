    !!! Generalized BAO module added by J. Dossett
    ! Copied structure from mpk.f90 and Reid BAO code
    !
    ! When using WiggleZ data set cite Blake et al. arXiv:1108.2635

    !for SDSS data set: http://www.sdss3.org/science/boss_publications.php

    ! For rescaling method see Hamann et al, http://arxiv.org/abs/1003.3999

    !AL/JH Oct 2012: encorporate DR9 data into something close to new cosmomc format
    !Dec 2013: merged in DR11 patch (Antonio J. Cuesta, for the BOSS collaboration)

    module bao
    use MatrixUtils
    use settings
    use CosmologyTypes
    use CosmoTheory
    use Calculator_Cosmology
    use Likelihood_Cosmology
    use IniObjects
    implicit none

    private

    type, extends(TCosmoCalcLikelihood) :: BAOLikelihood
        !    type, extends(TCosmoCalcLikelihood) :: BAOLikelihood
        integer :: num_bao ! total number of points used
        integer :: type_bao
        !what type of bao data is used
        !1: old sdss, no longer
        !2: A(z) =2 ie WiggleZ
        !3 D_V/rs in fitting forumla appox (DR9)
        !4: D_v - 6DF
        !5: D_A/rs (DR8)
        real(mcp), allocatable, dimension(:) :: bao_z, bao_obs, bao_err
        real(mcp), allocatable, dimension(:,:) :: bao_invcov


    contains
    procedure :: LogLike => BAO_LnLike
    procedure :: ReadIni => BAO_ReadIni
    procedure, private :: SDSS_dvtors
    procedure, private :: SDSS_dAtors
    procedure, private :: Acoustic
    procedure, private :: BAO_DR7_loglike
    procedure, private :: BAO_DR11_loglike
    end type BAOLikelihood

    integer,parameter :: DR11_alpha_npoints=280
    real(mcp), dimension (DR11_alpha_npoints) :: DR11_alpha_perp_file,DR11_alpha_plel_file
    real(mcp), dimension (DR11_alpha_npoints,DR11_alpha_npoints) ::   DR11_prob_file
    real(mcp) DR11_dalpha_perp, DR11_dalpha_plel
    real(mcp), dimension (10000) :: DR7_alpha_file, DR7_prob_file
    real(mcp) DR7_dalpha
    real rsdrag_theory
    real(mcp) :: BAO_fixed_rs = -1._mcp
    integer DR7_alpha_npoints

    logical :: MGS= .false.

    public BAOLikelihood, BAOLikelihood_Add
    contains

    subroutine BAOLikelihood_Add(LikeList, Ini)
    class(TLikelihoodList) :: LikeList
    class(TSettingIni) :: ini
    Type(BAOLikelihood), pointer :: this
    integer numbaosets, i

    if (Ini%Read_Logical('use_BAO',.false.)) then
        numbaosets = Ini%Read_Int('bao_numdatasets',0)
        if (numbaosets<1) call MpiStop('Use_BAO but numbaosets = 0')
        if (Ini%Haskey('BAO_fixed_rs')) then
            BAO_fixed_rs= Ini%Read_Double('BAO_fixed_rs',-1._mcp)
        end if
        do i= 1, numbaosets
            allocate(this)
            call this%ReadDatasetFile(Ini%ReadFileName(numcat('bao_dataset',i)))
            this%LikelihoodType = 'BAO'
            this%needs_background_functions = .true.
            call LikeList%Add(this)
        end do
        if (Feedback>1) write(*,*) 'read BAO data sets'
    end if

    end subroutine BAOLikelihood_Add

    subroutine BAO_ReadIni(this, Ini)
    class(BAOLikelihood) this
    class(TSettingIni) :: Ini
    character(LEN=:), allocatable :: bao_measurements_file, bao_invcov_file
    integer i,iopb
    Type(TTextFile) :: F

    if (Feedback > 0) write (*,*) 'reading BAO data set: '//trim(this%name)
    this%num_bao = Ini%Read_Int('num_bao',0)
    if (this%num_bao.eq.0) write(*,*) ' ERROR: parameter num_bao not set'
    this%type_bao = Ini%Read_Int('type_bao',1)
    if(this%type_bao /= 3 .and. this%type_bao /=2 .and. this%type_bao /=4 .and. this%type_bao /=5) then
        write(*,*) this%type_bao
        write(*,*)'ERROR: Invalid bao type specified in BAO dataset: '//trim(this%name)
        call MPIStop()
    end if

    allocate(this%bao_z(this%num_bao))
    allocate(this%bao_obs(this%num_bao))
    allocate(this%bao_err(this%num_bao))

    bao_measurements_file = Ini%ReadFileName('bao_measurements_file')
    call F%Open(bao_measurements_file)
    do i=1,this%num_bao
        read (F%unit,*, iostat=iopb) this%bao_z(i),this%bao_obs(i),this%bao_err(i)
    end do
    call F%Close()

    if (this%name == 'DR7') then
        !don't used observed value, probabilty distribution instead
        call BAO_DR7_init(Ini%ReadFileName('prob_dist'))
    elseif (this%name == 'DR11CMASS') then
        !don't used observed value, probabilty distribution instead
        call BAO_DR11_init(Ini%ReadFileName('prob_dist'))
    else
        allocate(this%bao_invcov(this%num_bao,this%num_bao))
        this%bao_invcov=0

        if (Ini%HasKey('bao_invcov_file')) then
            bao_invcov_file  = Ini%ReadFileName('bao_invcov_file')
            call File%ReadTextMatrix(bao_invcov_file, this%bao_invcov)
        else
            do i=1,this%num_bao
                !diagonal, or actually just 1..
                this%bao_invcov(i,i) = 1/this%bao_err(i)**2
            end do
        end if
    end if

    end subroutine BAO_ReadIni

    function Acoustic(this,CMB,z)
    class(BAOLikelihood) :: this
    class(CMBParams) CMB
    real(mcp) Acoustic
    real(mcp), intent(IN) :: z
    real(mcp) omh2,ckm,omegam,h

    omegam = 1.d0 - CMB%omv - CMB%omk
    h = CMB%h0/100
    ckm = const_c/1e3_mcp !JD c in km/s

    omh2 = omegam*h**2.d0
    Acoustic = 100*this%Calculator%BAO_D_v(z)*sqrt(omh2)/(ckm*z)
    end function Acoustic

    function SDSS_dvtors(this, CMB,z)
    !This uses numerical value of D_v/r_s, but re-scales it to match definition of SDSS
    !paper fitting at the fiducial model. Idea being it is also valid for e.g. varying N_eff
    class(BAOLikelihood) :: this
    class(CMBParams) CMB
    real(mcp) SDSS_dvtors
    real(mcp), intent(IN)::z
    real(mcp) rs
    real(mcp), parameter :: rs_rescale = 153.017d0/148.92 !149.0808

    !rs = SDSS_CMBToBAOrs(CMB)
    rs = rsdrag_theory*rs_rescale !rescaled to match fitting formula for LCDM
!print *, 'fiducial rs', rs
    SDSS_dvtors = this%Calculator%BAO_D_v(z)/rs

    end function SDSS_dvtors

   ! HS modified SDSS_dvtors to calculate D_A/rs 
    function SDSS_dAtors(this, CMB,z)
    !This uses numerical value of D_A/r_s, but re-scales it to match definition of SDSS
    !paper fitting at the fiducial model. Idea being it is also valid for e.g. varying N_eff
    class(BAOLikelihood) :: this
    class(CMBParams) CMB
    real(mcp) SDSS_dAtors
    real(mcp), intent(IN)::z
    real(mcp) rs
    real(mcp), parameter :: rs_rescale = 153.017d0/148.92 !149.0808

    !    rs = SDSS_CMBToBAOrs(CMB)
    rs = rsdrag_theory*rs_rescale !rescaled to match fitting formula for LCDM
    SDSS_dAtors = this%Calculator%AngularDiameterDistance(z)/rs
!print *, 'fiducial rs', rs
    end function SDSS_dAtors


    !===================================================================================

    function BAO_LnLike(this, CMB, Theory, DataParams)
    Class(BAOLikelihood) :: this
    Class(CMBParams) CMB
    Class(TCosmoTheoryPredictions), target :: Theory
    real(mcp) :: DataParams(:)
    integer j,k
    real(mcp) BAO_LnLike
    real(mcp), allocatable :: BAO_theory(:)

    if (BAO_fixed_rs>0) then
        !this is just for use for e.g. BAO 'only' constraints
        rsdrag_theory =  BAO_fixed_rs
    else
        rsdrag_theory =  Theory%derived_parameters( derived_rdrag )
    end if
    BAO_LnLike=0
    if (this%name=='DR7') then
        BAO_LnLike = this%BAO_DR7_loglike(CMB,this%bao_z(1))
    elseif (this%name=='DR11CMASS') then
        BAO_LnLike = this%BAO_DR11_loglike(CMB,this%bao_z(1))
    else
        allocate(BAO_theory(this%num_bao))

        if(this%type_bao ==3)then
            do j=1, this%num_bao
                BAO_theory(j) = this%SDSS_dvtors(CMB,this%bao_z(j))
            end do
        else if(this%type_bao ==2)then
            do j=1, this%num_bao
                BAO_theory(j) = this%Acoustic(CMB,this%bao_z(j))
            end do
        else if(this%type_bao ==4)then
            do j=1, this%num_bao
                BAO_theory(j) = this%Calculator%BAO_D_v(this%bao_z(j))
            end do
        else if(this%type_bao ==5)then
            do j=1, this%num_bao
                BAO_theory(j) = this%SDSS_dAtors(CMB,this%bao_z(j))
            end do

        end if

        do j=1, this%num_bao
            do k=1, this%num_bao
                BAO_LnLike = BAO_LnLike +&
                (BAO_theory(j)-this%bao_obs(j))*this%bao_invcov(j,k)*&
                (BAO_theory(k)-this%bao_obs(k))
            end do
        end do
        BAO_LnLike = BAO_LnLike/2.d0

        deallocate(BAO_theory)
    end if

    if(feedback>1) write(*,*) trim(this%name)//' BAO likelihood = ', BAO_LnLike

    end function BAO_LnLike


    subroutine BAO_DR7_init(fname)
    character(LEN=*), intent(in) :: fname
    real(mcp) :: tmp0,tmp1
    real(mcp) :: DR7_alpha =0
    integer ios,ii

    open(unit=7,file=fname,status='old')
    !Read data file
    ios = 0
    ii  = 0
    do while (ios.eq.0)
        read (7,*,iostat=ios) tmp0,tmp1
        if (ios .ne. 0) cycle
        if((ii.gt.1).and.(abs(DR7_dalpha-(tmp0-DR7_alpha)).gt.1e-6)) then
            stop 'binning should be uniform in sdss_baoDR7.txt'
        endif
        ii = ii+1
        DR7_alpha_file(ii) = tmp0
        DR7_prob_file (ii) = tmp1
        DR7_dalpha = tmp0-DR7_alpha
        DR7_alpha  = tmp0
    enddo
    DR7_alpha_npoints = ii
    if (ii.eq.0) call MpiStop('ERROR : reading file')
    close(7)
    !Normalize distribution (so that the peak value is 1.0)
    tmp0=0.0
    do ii=1,DR7_alpha_npoints
        if(DR7_prob_file(ii).gt.tmp0) then
            tmp0=DR7_prob_file(ii)
        endif
    enddo
    DR7_prob_file=DR7_prob_file/tmp0

    end subroutine BAO_DR7_init

    function BAO_DR7_loglike(this,CMB,z)
    Class(BAOLikelihood) :: this
    Class(CMBParams) CMB
    real (mcp) z, BAO_DR7_loglike, alpha_chain, prob
    real,parameter :: rs_wmap7=152.7934d0,dv1_wmap7=1340.177  !r_s and D_V computed for wmap7 cosmology
    integer ii
    alpha_chain = (this%SDSS_dvtors(CMB,z))/(dv1_wmap7/rs_wmap7)
    if ((alpha_chain.gt.DR7_alpha_file(DR7_alpha_npoints-1)).or.(alpha_chain.lt.DR7_alpha_file(1))) then
        BAO_DR7_loglike = logZero
    else
        ii=1+floor((alpha_chain-DR7_alpha_file(1))/DR7_dalpha)
        prob=DR7_prob_file(ii)+(DR7_prob_file(ii+1)-DR7_prob_file(ii))/ &
        (DR7_alpha_file(ii+1)-DR7_alpha_file(ii))*(alpha_chain-DR7_alpha_file(ii))
        BAO_DR7_loglike = -log( prob )
    endif

    end function BAO_DR7_loglike

    subroutine BAO_DR11_init(fname)
    character(LEN=*), intent(in) :: fname
    real(mcp) :: tmp0,tmp1,tmp2
    integer ios,ii,jj,nn

    open(unit=7,file=fname,status='old')
    ios = 0
    nn=0
    do while (ios.eq.0)
        read (7,*,iostat=ios) tmp0,tmp1,tmp2
        if (ios .ne. 0) cycle
        nn = nn + 1
        ii = 1 +     (nn-1)/DR11_alpha_npoints
        jj = 1 + mod((nn-1),DR11_alpha_npoints)
        DR11_alpha_perp_file(ii)   = tmp0
        DR11_alpha_plel_file(jj)   = tmp1
        DR11_prob_file(ii,jj)      = tmp2
    enddo
    close(7)
    DR11_dalpha_perp=DR11_alpha_perp_file(2)-DR11_alpha_perp_file(1)
    DR11_dalpha_plel=DR11_alpha_plel_file(2)-DR11_alpha_plel_file(1)
    !Normalize distribution (so that the peak value is 1.0)
    tmp0=0.0
    do ii=1,DR11_alpha_npoints
        do jj=1,DR11_alpha_npoints
            if(DR11_prob_file(ii,jj).gt.tmp0) then
                tmp0=DR11_prob_file(ii,jj)
            endif
        enddo
    enddo
    DR11_prob_file=DR11_prob_file/tmp0

    end subroutine BAO_DR11_init

    function BAO_DR11_loglike(this,CMB,z)
    Class(BAOLikelihood) :: this
    Class(CMBParams) CMB
    real (mcp) z, BAO_DR11_loglike, alpha_perp, alpha_plel, prob
    real,parameter :: rd_fid=149.28,H_fid=93.558,DA_fid=1359.72 !fiducial parameters
    integer ii,jj

    ! LS I added this
    real, dimension(399) :: DR7_prob
    real (mcp) zdr7, rsfiddr7, DVfiddr7, Hdr7, DAdr7, DVdr7, alphadr7, chi2


    alpha_perp=(this%Calculator%AngularDiameterDistance(z)/rsdrag_theory)/(DA_fid/rd_fid)
    alpha_plel=(H_fid*rd_fid)/((const_c*this%Calculator%Hofz(z)/1.d3)*rsdrag_theory)
    if ((alpha_perp.lt.DR11_alpha_perp_file(1)).or.(alpha_perp.gt.DR11_alpha_perp_file(DR11_alpha_npoints-1)).or. &
    &   (alpha_plel.lt.DR11_alpha_plel_file(1)).or.(alpha_plel.gt.DR11_alpha_plel_file(DR11_alpha_npoints-1))) then
        BAO_DR11_loglike = logZero
    else
        ii=1+floor((alpha_perp-DR11_alpha_perp_file(1))/DR11_dalpha_perp)
        jj=1+floor((alpha_plel-DR11_alpha_plel_file(1))/DR11_dalpha_plel)
        prob=(1./((DR11_alpha_perp_file(ii+1)-DR11_alpha_perp_file(ii))*(DR11_alpha_plel_file(jj+1)-DR11_alpha_plel_file(jj))))*  &
        &       (DR11_prob_file(ii,jj)*(DR11_alpha_perp_file(ii+1)-alpha_perp)*(DR11_alpha_plel_file(jj+1)-alpha_plel) &
        &       -DR11_prob_file(ii+1,jj)*(DR11_alpha_perp_file(ii)-alpha_perp)*(DR11_alpha_plel_file(jj+1)-alpha_plel) &
        &       -DR11_prob_file(ii,jj+1)*(DR11_alpha_perp_file(ii+1)-alpha_perp)*(DR11_alpha_plel_file(jj)-alpha_plel) &
        &       +DR11_prob_file(ii+1,jj+1)*(DR11_alpha_perp_file(ii)-alpha_perp)*(DR11_alpha_plel_file(jj)-alpha_plel))
        if  (prob.gt.0.) then
            BAO_DR11_loglike = -log( prob )
        else
            BAO_DR11_loglike = logZero
        endif
    endif



                  !MGS is used everythime CMASS is called
    if(MGS) then
        print *, "using MGS_BAO"

     DR7_prob = (/8.54783189353, 7.80363740636, 7.7078667921, 7.74064378608, &
7.78165406477, 7.8259614948, 7.8720123764, 7.9177992356, 7.96404102881, &
8.00969768306, 8.05491712654, 8.09985440568, 8.14440116619, 8.18911894508, &
8.23329124549, 8.27684696027, 8.31999823329, 8.36235072513, 8.40404247144, &
8.44538116734, 8.48615435217, 8.52614100695, 8.56553128113, 8.6042868491, &
8.64224123379, 8.67933258138, 8.7155104155, 8.75075978816, 8.78530434174, &
8.81937724671, 8.85269159757, 8.88495211807, 8.91643361704, 8.94713610169, &
8.97656381574, 9.0050815866, 9.03296539494, 9.05989718311, 9.0858169855, &
9.11066260557, 9.13465887895, 9.15764904155, 9.17938311136, 9.20059138282, &
9.22027661365, 9.23934898941, 9.25775022638, 9.27496230622, 9.29121425635, &
9.30645925043, 9.32063058823, 9.33352231645, 9.34522862569, 9.35627179232, &
9.36615966655, 9.37483770168, 9.38256369487, 9.3886318045, 9.39404329252, &
9.39812192501, 9.40110672901, 9.40313278078, 9.40406521705, 9.40393504588, &
9.40260032617, 9.4000988632, 9.39667841599, 9.3919005596, 9.38592365276, &
9.37868956925, 9.37045124505, 9.36118122596, 9.35073440239, 9.3390037054, &
9.32590808917, 9.31170814578, 9.29642849303, 9.28001937076, 9.26270859072, &
9.24433521208, 9.22478576261, 9.20392704025, 9.1819356519, 9.15902788896, &
9.13480561153, 9.10947247524, 9.08281985539, 9.05486095484, 9.02609969454, &
8.99634116098, 8.9653392987, 8.93301990966, 8.89928320536, 8.86491711752, &
8.82907205622, 8.79268386806, 8.75528485149, 8.71668001126, 8.67696874299, &
8.63605522065, 8.59402648319, 8.55108855542, 8.50697408074, 8.46184989833, &
8.41533830259, 8.36756753452, 8.31911910346, 8.26939003554, 8.21876554316, &
8.16671538875, 8.11340358936, 8.05917481447, 8.00397594095, 7.94826070343, &
7.89162366923, 7.83391284201, 7.77505016298, 7.71501532701, 7.65396121075, &
7.59226950453, 7.5294792078, 7.46559235421, 7.4006547252, 7.33460559286, &
7.26756710251, 7.19990677439, 7.13128012494, 7.06145747261, 6.99060174279, &
6.91878570821, 6.84607818385, 6.77290107174, 6.6993119727, 6.62488860071, &
6.54927010747, 6.47272325675, 6.39543889501, 6.31731535149, 6.23878965634, &
6.15933036128, 6.07923666599, 5.99823951263, 5.91615697769, 5.83393838811, &
5.75095932915, 5.66748765923, 5.58326500466, 5.4981944684, 5.41260127189, &
5.32644546473, 5.24053993441, 5.15433315616, 5.06751500344, 4.98028740999, &
4.89246810803, 4.80451344258, 4.71656621894, 4.62833599084, 4.54024278927, &
4.45187870621, 4.36329446879, 4.27456510031, 4.18585106142, 4.09752677098, &
4.00918757545, 3.92092480158, 3.83275636798, 3.74439887622, 3.65616165324, &
3.56876517476, 3.48186680769, 3.39508397711, 3.30843088223, 3.22202868653, &
3.13614474119, 3.05055869207, 2.96578080679, 2.88151202379, 2.7978246659, &
2.71481035642, 2.63234027274, 2.55039083236, 2.46949642172, 2.38950629832, &
2.31036571268, 2.23219631551, 2.15483829989, 2.07813885357, 2.00253618695, &
1.92838221561, 1.8554552856, 1.78340455334, 1.71213856629, 1.6424543125, &
1.57351544613, 1.50588148358, 1.43963661044, 1.37447753167, 1.31064900901, &
1.24804862436, 1.18658618905, 1.1262474879, 1.06729612571, 1.00986790209, &
0.95386553601, 0.899287378725, 0.84630676967, 0.79404515997, 0.74375269023, &
0.695089066235, 0.64797667677, 0.60243828145, 0.558423499255, 0.51606601867, &
0.47526823274, 0.435952933675, 0.398538587708, 0.362777592055, 0.328713295642, &
0.296511727028, 0.265951840778, 0.237039752705, 0.209957360948, 0.184623327035,&
0.161095383987, 0.13945807601, 0.1195620184, 0.101129587065, 0.0842916850675, &
0.0690570828475, 0.0553837389525, 0.0432035435875, 0.03261004133, &
0.0236626057875, 0.016039579325, 0.0098741431575, 0.0051346324425, &
0.00195625218, 0.0003090468525, 0.0, 0.001356666915, 0.00418939496, &
0.0083542271875, 0.014341447905, 0.0214889687125, 0.0305225695775, &
0.0411771475625, 0.053302156825, 0.0669813308725, 0.082094926745, &
0.0984418731725, 0.116211841033, 0.135393671815, 0.156206717222, 0.17839654088,&
0.20179905741, 0.226727008378, 0.252425908275, 0.279866794063, 0.308437572653, &
0.338151394477, 0.369188876978, 0.401487150298, 0.4348946805, 0.469341766138, &
0.50492108416, 0.541724995835, 0.579532591495, 0.618497015585, 0.65849273713, &
0.699382999618, 0.740834296265, 0.78301772296, 0.826163713635, 0.870099235403, &
0.915068839168, 0.960778275205, 1.00713621884, 1.05424451771, 1.10202516995, &
1.15058947938, 1.19972327183, 1.24963054841, 1.3003609346, 1.35178403682, &
1.40389053651, 1.45651100492, 1.50990858059, 1.56394744178, 1.61861404719, &
1.67395499856, 1.72991919923, 1.78610301827, 1.84261663227, 1.89917336731, &
1.95623074639, 2.0136942887, 2.07159979263, 2.12970653652, 2.18804345098, &
2.24635688461, 2.30467622227, 2.36309571084, 2.42156667293, 2.47996538491, &
2.53852297474, 2.59736654731, 2.65588460606, 2.71468930435, 2.77355996939, &
2.83192697012, 2.89069907425, 2.94948128007, 3.00846174359, 3.06724832725, &
3.12564361281, 3.1838691566, 3.24200543961, 3.30016373794, 3.35853145702, &
3.41677769154, 3.47492124035, 3.5328589123, 3.59049654316, 3.64789490381, &
3.70508293831, 3.76197283876, 3.81855938603, 3.8751013311, 3.93135914147, &
3.98717887017, 4.04276516233, 4.09795571306, 4.15275906475, 4.20714567797, &
4.26130235367, 4.31515938742, 4.36832249701, 4.42090187038, 4.47301187827, &
4.52487284508, 4.57644221529, 4.62788971928, 4.67922637271, 4.73002796479, &
4.78041296001, 4.83024601166, 4.87965682781, 4.92867726272, 4.97718525341, &
5.02526581479, 5.07307544714, 5.12037213745, 5.16723654138, 5.21355158379, &
5.25930449458, 5.3045506524, 5.3490549876, 5.39335716842, 5.43708834636, &
5.48007726993, 5.52240750361, 5.56419393346, 5.60555990147, 5.64652029038, &
5.68731528687, 5.72771509841, 5.76758360989, 5.80686703681, 5.84547791465, &
5.88350608105, 5.92098452623, 5.9577903618, 5.9939662751, 6.02954953263, &
6.06456263004, 6.09895033869, 6.13270515143, 6.16577526729, 6.19813137433, &
6.2297891072, 6.26081796305, 6.29138584252, 6.32131382214, 6.35047918818, &
6.37899783829, 6.40704355069, 6.43453754268, 6.46167887271, 6.4885476412, &
6.51501289515, 6.54081517743, 6.56590390895, 6.5904091308, 6.6142295692, &
6.63755929446, 6.66019321587, 6.68214613365, 6.70356436671 /)

    zdr7 = 0.15
    rsfiddr7 = 148.69
    DVfiddr7 = 638.9518
    Hdr7 = (const_c*this%Calculator%Hofz(zdr7)/1.d3)
!this%Calculator%Hofz(zdr7)*const_c/1000.0
    DAdr7 = this%Calculator%AngularDiameterDistance(zdr7)
!this%Calculator%AngularDiameterDistance(zdr7)
    DVdr7 = (DAdr7**2*const_c/1000.0*0.15*1.15**2/Hdr7)**(1.0/3.0)
    alphadr7 = DVdr7 / rsdrag_theory / (DVfiddr7 / rsfiddr7)
    !print *, 'LS', zdr7, alphadr7, DVdr7, DAdr7, const_c, Hdr7, rsdrag_theory 
      if ((alphadr7.lt.0.8005).or.(alphadr7.gt.1.1985)) then
        BAO_DR11_loglike = BAO_DR11_loglike + logZero
      else
        ii = 1+floor((alphadr7 - 0.8005)/0.001)
        chi2 = (DR7_prob(ii) + DR7_prob(ii+1))/2.0
        BAO_DR11_loglike = BAO_DR11_loglike + chi2/2.0
      endif


   if(feedback>1) write(*,*), 'MGS+CMASS BAO likelihood = ', BAO_DR11_loglike

    endif



    end function BAO_DR11_loglike

    function SDSS_CMBToBAOrs(CMB)
    Type(CMBParams) CMB
    real(mcp) ::  rsdrag
    real(mcp) :: SDSS_CMBToBAOrs
    real(mcp) :: zeq,zdrag,omh2,obh2,b1,b2
    real(mcp) :: rd,req,wkeq

    obh2=CMB%ombh2
    omh2=CMB%ombh2+CMB%omdmh2

    b1     = 0.313*omh2**(-0.419)*(1+0.607*omh2**0.674)
    b2     = 0.238*omh2**0.223
    zdrag  = 1291.*omh2**0.251*(1.+b1*obh2**b2)/(1.+0.659*omh2**0.828)
    zeq    = 2.50e4*omh2*(2.726/2.7)**(-4.)
    wkeq   = 7.46e-2*omh2*(2.726/2.7)**(-2)
    req    = 31.5*obh2*(2.726/2.7)**(-4)*(1e3/zeq)
    rd     = 31.5*obh2*(2.726/2.7)**(-4)*(1e3/zdrag)
    rsdrag = 2./(3.*wkeq)*sqrt(6./req)*log((sqrt(1.+rd)+sqrt(rd+req))/(1.+sqrt(req)))

    SDSS_CMBToBAOrs = rsdrag

    end function SDSS_CMBToBAOrs


    end module bao
